from modules.base import BaseModule

class Product(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "Product Module"
        self.routes = []
    
    def initialize(self, db_conn, shared_context):
        print(f"Initializing {self.name} with database...")
        self.db_conn = db_conn
        self.shared_context = shared_context
        self.create_products_table()
        
        
        return self

    def deinitialize(self):
        try:
            if hasattr(self, 'db_conn') and self.db_conn:
                cursor = self.db_conn.cursor()
                cursor.execute("DELETE FROM products")
                self.db_conn.commit()
                cursor.close()
                self.db_conn.close()
                print(f"Deinitialized {self.name} database connection")
        except Exception as e:
            print(f"Error during deinitialization of {self.name}: {e}")
            raise
        finally:
            return self
    
    
    def load_routes(self):
        self.routes = [
            ("/products", self.list_products, "GET"),
            ("/products/add", self.add_product_handler, "POST"),
            ("/products/delete", self.delete_product_handler, "POST")
        ]
        return self.routes
    
    def create_products_table(self) -> bool:
        try:
            print("Creating products table...")
            cursor = self.db_conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS products
                            (id INTEGER PRIMARY KEY, name TEXT, price REAL, category TEXT)''')
            self.db_conn.commit()
            print("Products table created successfully")
            cursor.close()
            return True
        except Exception as e:
            print(f"Error creating products table: {e}")
            return False
    
    
    def add_product_handler(self, environ, start_response):
        body = self.get_body(environ)
        if body is None:
            return self.response(start_response, {"error": "Invalid JSON data"})
        if not body:
            return self.response(start_response, {"error": "No data provided"})
        cursor = self.db_conn.cursor()
        cursor.execute("INSERT INTO products (name, price, category) VALUES (?, ?, ?)", (body.get('name'), body.get('price'), body.get('category')))
        self.db_conn.commit()
        cursor.close()
        return self.response(start_response, {"message": "Product added successfully"})

    def delete_product_handler(self, environ, start_response):
        params = self.get_params(environ)
        cursor = self.db_conn.cursor()
        cursor.execute("DELETE FROM products WHERE id = ?", (params.get('id'),))
        self.db_conn.commit()
        cursor.close()
        return self.response(start_response, {"message": "Product removed successfully"})

    def list_products(self, environ, start_response):
        try:
            cursor = self.db_conn.cursor()
            cursor.execute("SELECT * FROM products")
            products = cursor.fetchall()
            cursor.close()
            
            product_list = []
            for product in products:
                product_list.append({
                    'id': product[0],
                    'name': product[1],
                    'price': product[2],
                    'category': product[3]
                })
            
            return self.response(start_response, product_list)
        except Exception as e:
            print(f"Error listing products: {e}")
            return self.response(start_response, [{'error': 'Failed to list products'}])
        