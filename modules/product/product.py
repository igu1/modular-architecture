class Product:
    def __init__(self):
        self.name = "Product Module"
    
    def initialize(self, db_conn, shared_context):
        print(f"Initializing {self.name} with database...")
        self.db_conn = db_conn
        self.shared_context = shared_context
        self.create_products_table()
        
        # Set up event listeners
        if 'event_dispatcher' in self.shared_context:
            self.shared_context['event_dispatcher']['on']('product_list', self.on_product_list)
            self.shared_context['event_dispatcher']['on']('product_get', self.on_product_get)
        
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
    
    def add_product(self, name: str, price: float, category: str) -> bool:
        try:
            cursor = self.db_conn.cursor()
            cursor.execute("INSERT INTO products (name, price, category) VALUES (?, ?, ?)", 
                         (name, price, category))
            self.db_conn.commit()
            product_id = cursor.lastrowid
            cursor.close()
            
            # Emit product added event
            if 'event_dispatcher' in self.shared_context:
                self.shared_context['event_dispatcher']['emit']('product_added', {
                    'id': product_id,
                    'name': name,
                    'price': price,
                    'category': category
                })
            
            print(f"Product '{name}' added successfully with ID: {product_id}")
            return True
        except Exception as e:
            print(f"Error adding product: {e}")
            return False
    
    def get_product(self, product_id: int):
        try:
            cursor = self.db_conn.cursor()
            cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
            product = cursor.fetchone()
            cursor.close()
            return product
        except Exception as e:
            print(f"Error getting product: {e}")
            return None
    
    def list_products(self):
        try:
            cursor = self.db_conn.cursor()
            cursor.execute("SELECT * FROM products")
            products = cursor.fetchall()
            cursor.close()
            return products
        except Exception as e:
            print(f"Error listing products: {e}")
            return []
    
    def on_product_list(self, payload, context):
        print(f"Product module received list event: {payload}")
        products = self.list_products()
        print(f"Available products: {products}")
        return products
    
    def on_product_get(self, payload, context):
        print(f"Product module received get event: {payload}")
        product_id = payload.get('id')
        if product_id:
            product = self.get_product(product_id)
            print(f"Product details: {product}")
            return product
        return None
