from modules.base import BaseModule

class Cart(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "Shopping Cart Module"
        self.dependencies = ["product"]
        self.routes = []
    
    def initialize(self, db_conn, shared_context):
        print(f"Initializing {self.name} with database...")
        self.db_conn = db_conn
        self.shared_context = shared_context
        
        self.create_table()
        
        return self

    def load_routes(self):
        routes = [
            ("/cart/view", self.view_cart, "GET"),
            ("/cart/add", self.add_to_cart, "POST"),
        ]
        self.routes.extend(routes)
        return routes

    def deinitialize(self):
        try:
            if hasattr(self, 'db_conn') and self.db_conn:
                cursor = self.db_conn.cursor()
                cursor.execute("DELETE FROM cart")
                self.db_conn.commit()
                cursor.close()
                self.db_conn.close()
                print(f"Deinitialized {self.name} database connection")
        except Exception as e:
            print(f"Error during deinitialization of {self.name}: {e}")
            raise
        finally:
            return self
    
    def add_to_cart(self, environ, start_response):
        body = self.get_body(environ)
        if not body:
            return self.response(start_response, {"error": "No data provided"})
        
        cursor = self.db_conn.cursor()
        product_id = body.get('product_id', [None])[0]
        quantity = body.get('quantity', [1])[0]
        price = body.get('price', [0.0])[0]
        
        cursor.execute("INSERT INTO cart (product_id, quantity, price) VALUES (?, ?, ?)", (product_id, quantity, price))
        self.db_conn.commit()
        cursor.close()
        return self.response(start_response, {"success": True, "message": "Item added to cart"})

    def view_cart(self, environ, start_response):
        try:
            cursor = self.db_conn.cursor()
            cursor.execute('''SELECT c.id, c.product_id, c.quantity, c.price, p.name, p.category 
                            FROM cart c 
                            LEFT JOIN products p ON c.product_id = p.id''')
            cart_items = cursor.fetchall()
            cursor.close()
            
            total = sum(item[2] * item[3] for item in cart_items)
            
            response_data = {
                'items': cart_items,
                'total': total,
                'item_count': len(cart_items),
                'success': True
            }
            
            return self.response(start_response, response_data)
        except Exception as e:
            print(f"Error viewing cart: {e}")
            return self.response(start_response, {'items': [], 'total': 0, 'item_count': 0, 'error': str(e), 'success': False})
    
    def create_table(self):
        try:
            cursor = self.db_conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS cart (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_id INTEGER NOT NULL,
                    quantity INTEGER NOT NULL DEFAULT 1,
                    price REAL NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (product_id) REFERENCES products(id)
                )
            ''')
            self.db_conn.commit()
            cursor.close()
            return {"success": True, "message": "Cart table created"}
        except Exception as e:
            print(f"Error creating cart table: {e}")
            return {"success": False, "error": str(e)}