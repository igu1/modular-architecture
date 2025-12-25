class Cart:
    def __init__(self):
        self.name = "Shopping Cart Module"
        self.dependencies = ["product"]
    
    def initialize(self, db_conn, shared_context):
        print(f"Initializing {self.name} with database...")
        self.db_conn = db_conn
        self.shared_context = shared_context
        self.create_cart_table()
        
        # Set up event listeners
        if 'event_dispatcher' in self.shared_context:
            self.shared_context['event_dispatcher']['on']('cart_add', self.on_cart_add)
            self.shared_context['event_dispatcher']['on']('cart_remove', self.on_cart_remove)
            self.shared_context['event_dispatcher']['on']('cart_view', self.on_cart_view)
            self.shared_context['event_dispatcher']['on']('cart_clear', self.on_cart_clear)
        
        return self

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
        
    def create_cart_table(self) -> bool:
        try:
            print("Creating cart table...")
            cursor = self.db_conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS cart
                            (id INTEGER PRIMARY KEY, product_id INTEGER, quantity INTEGER, 
                             price REAL, added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
            self.db_conn.commit()
            print("Cart table created successfully")
            cursor.close()
            return True
        except Exception as e:
            print(f"Error creating cart table: {e}")
            return False
    
    def add_to_cart(self, product_id: int, quantity: int = 1) -> bool:
        try:
            # Check if product exists
            loaded_modules = self.shared_context.get('loaded_modules', {})
            product_module = loaded_modules.get('product')
            if not product_module:
                print("Product module not available")
                return False
            
            product = product_module.get_product(product_id)
            if not product:
                print(f"Product with ID {product_id} not found")
                return False
            
            cursor = self.db_conn.cursor()
            # Check if product already in cart
            cursor.execute("SELECT * FROM cart WHERE product_id = ?", (product_id,))
            existing_item = cursor.fetchone()
            
            if existing_item:
                # Update quantity
                new_quantity = existing_item[2] + quantity
                cursor.execute("UPDATE cart SET quantity = ? WHERE product_id = ?", 
                             (new_quantity, product_id))
            else:
                # Add new item
                cursor.execute("INSERT INTO cart (product_id, quantity, price) VALUES (?, ?, ?)", 
                             (product_id, quantity, product[2]))  # product[2] is price
            
            self.db_conn.commit()
            cursor.close()
            
            # Emit cart updated event
            if 'event_dispatcher' in self.shared_context:
                self.shared_context['event_dispatcher']['emit']('cart_updated', {
                    'product_id': product_id,
                    'quantity': quantity,
                    'action': 'added'
                })
            
            print(f"Added {quantity} of product ID {product_id} to cart")
            return True
        except Exception as e:
            print(f"Error adding to cart: {e}")
            return False
    
    def remove_from_cart(self, product_id: int, quantity: int = None) -> bool:
        try:
            cursor = self.db_conn.cursor()
            
            if quantity is None:
                # Remove entire item
                cursor.execute("DELETE FROM cart WHERE product_id = ?", (product_id,))
                action = 'removed'
            else:
                # Reduce quantity
                cursor.execute("SELECT quantity FROM cart WHERE product_id = ?", (product_id,))
                existing = cursor.fetchone()
                if existing and existing[0] > quantity:
                    new_quantity = existing[0] - quantity
                    cursor.execute("UPDATE cart SET quantity = ? WHERE product_id = ?", 
                                 (new_quantity, product_id))
                    action = 'quantity_reduced'
                else:
                    # Remove if quantity would be 0 or less
                    cursor.execute("DELETE FROM cart WHERE product_id = ?", (product_id,))
                    action = 'removed'
            
            self.db_conn.commit()
            cursor.close()
            
            # Emit cart updated event
            if 'event_dispatcher' in self.shared_context:
                self.shared_context['event_dispatcher']['emit']('cart_updated', {
                    'product_id': product_id,
                    'quantity': quantity,
                    'action': action
                })
            
            print(f"Removed product ID {product_id} from cart")
            return True
        except Exception as e:
            print(f"Error removing from cart: {e}")
            return False
    
    def view_cart(self):
        try:
            cursor = self.db_conn.cursor()
            cursor.execute('''SELECT c.product_id, c.quantity, c.price, p.name, p.category 
                            FROM cart c 
                            LEFT JOIN products p ON c.product_id = p.id''')
            cart_items = cursor.fetchall()
            cursor.close()
            
            # Calculate total
            total = sum(item[1] * item[2] for item in cart_items)
            
            return {
                'items': cart_items,
                'total': total,
                'item_count': len(cart_items)
            }
        except Exception as e:
            print(f"Error viewing cart: {e}")
            return {'items': [], 'total': 0, 'item_count': 0}
    
    def clear_cart(self) -> bool:
        try:
            cursor = self.db_conn.cursor()
            cursor.execute("DELETE FROM cart")
            self.db_conn.commit()
            cursor.close()
            
            # Emit cart cleared event
            if 'event_dispatcher' in self.shared_context:
                self.shared_context['event_dispatcher']['emit']('cart_cleared', {})
            
            print("Cart cleared successfully")
            return True
        except Exception as e:
            print(f"Error clearing cart: {e}")
            return False
    
    def get_cart_total(self) -> float:
        cart_data = self.view_cart()
        return cart_data['total']
    
    # Event handlers
    def on_cart_add(self, payload, context):
        print(f"Cart module received add event: {payload}")
        product_id = payload.get('product_id')
        quantity = payload.get('quantity', 1)
        if product_id:
            self.add_to_cart(product_id, quantity)
    
    def on_cart_remove(self, payload, context):
        print(f"Cart module received remove event: {payload}")
        product_id = payload.get('product_id')
        quantity = payload.get('quantity')
        if product_id:
            self.remove_from_cart(product_id, quantity)
    
    def on_cart_view(self, payload, context):
        print(f"Cart module received view event: {payload}")
        cart_data = self.view_cart()
        print(f"Cart contents: {cart_data}")
        return cart_data
    
    def on_cart_clear(self, payload, context):
        print(f"Cart module received clear event: {payload}")
        self.clear_cart()
