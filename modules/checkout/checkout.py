import uuid
from datetime import datetime

class Checkout:
    def __init__(self):
        self.name = "Checkout Module"
        self.dependencies = ["cart"]
        
    
    def initialize(self, db_conn, shared_context):
        print(f"Initializing {self.name} with database...")
        self.db_conn = db_conn
        self.shared_context = shared_context
        self.create_orders_table()
        
        self.shared_context['event_dispatcher']['on']('checkout_start', self.on_checkout_start)
        self.shared_context['event_dispatcher']['on']('payment_process', self.on_payment_process)
        self.shared_context['event_dispatcher']['on']('order_complete', self.on_order_complete)
        
        return self

    def deinitialize(self):
        try:
            if hasattr(self, 'db_conn') and self.db_conn:
                cursor = self.db_conn.cursor()
                cursor.execute("DELETE FROM orders")
                self.db_conn.commit()
                cursor.close()
                self.db_conn.close()
                print(f"Deinitialized {self.name} database connection")
        except Exception as e:
            print(f"Error during deinitialization of {self.name}: {e}")
            raise
        finally:
            return self
        
    def create_orders_table(self) -> bool:
        try:
            print("Creating orders table...")
            cursor = self.db_conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS orders
                            (id INTEGER PRIMARY KEY, order_id TEXT UNIQUE, 
                             total_amount REAL, status TEXT, payment_method TEXT,
                             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
            
            cursor.execute('''CREATE TABLE IF NOT EXISTS order_items
                            (id INTEGER PRIMARY KEY, order_id TEXT, 
                             product_id INTEGER, quantity INTEGER, price REAL,
                             product_name TEXT, product_category TEXT)''')
            
            self.db_conn.commit()
            print("Orders tables created successfully")
            cursor.close()
            return True
        except Exception as e:
            print(f"Error creating orders table: {e}")
            return False
    
    def start_checkout(self, payment_method="credit_card") -> dict:
        try:
            # Get cart contents
            loaded_modules = self.shared_context.get('loaded_modules', {})
            cart_module = loaded_modules.get('cart')
            if not cart_module:
                return {'success': False, 'error': 'Cart module not available'}
            
            cart_data = cart_module.view_cart()
            if not cart_data['items']:
                return {'success': False, 'error': 'Cart is empty'}
            
            # Generate order ID
            order_id = str(uuid.uuid4())[:8].upper()
            
            # Emit checkout start event
            self.shared_context['event_dispatcher']['emit']('checkout_start', {
                'order_id': order_id,
                'cart_data': cart_data,
                'payment_method': payment_method
            })
            
            return {
                'success': True,
                'order_id': order_id,
                'cart_data': cart_data,
                'total_amount': cart_data['total']
            }
        except Exception as e:
            print(f"Error starting checkout: {e}")
            return {'success': False, 'error': str(e)}
    
    def process_payment(self, order_id: str, payment_method: str = "credit_card") -> dict:
        try:
            # Simulate payment processing
            print(f"Processing payment for order {order_id} using {payment_method}...")
            
            # Simulate payment delay
            import time
            time.sleep(1)  # Simulate processing time
            
            # Dummy payment logic (always succeeds for demo)
            payment_success = True
            transaction_id = f"TXN{uuid.uuid4().hex[:10].upper()}"
            
            # Emit payment process event
            self.shared_context['event_dispatcher']['emit']('payment_process', {
                'order_id': order_id,
                'payment_method': payment_method,
                'success': payment_success,
                'transaction_id': transaction_id
                })
            
            if payment_success:
                return {
                    'success': True,
                    'transaction_id': transaction_id,
                    'message': 'Payment processed successfully'
                }
            else:
                return {
                    'success': False,
                    'error': 'Payment failed'
                }
        except Exception as e:
            print(f"Error processing payment: {e}")
            return {'success': False, 'error': str(e)}
    
    def complete_order(self, order_id: str, cart_data: dict, transaction_id: str) -> dict:
        try:
            cursor = self.db_conn.cursor()
            
            # Insert order
            cursor.execute('''INSERT INTO orders (order_id, total_amount, status, payment_method)
                            VALUES (?, ?, ?, ?)''',
                         (order_id, cart_data['total'], 'completed', 'credit_card'))
            
            # Insert order items
            for item in cart_data['items']:
                cursor.execute('''INSERT INTO order_items 
                                (order_id, product_id, quantity, price, product_name, product_category)
                                VALUES (?, ?, ?, ?, ?, ?)''',
                             (order_id, item[0], item[1], item[2], item[3], item[4]))
            
            self.db_conn.commit()
            cursor.close()
            
            # Clear cart after successful order
            loaded_modules = self.shared_context.get('loaded_modules', {})
            cart_module = loaded_modules.get('cart')
            if cart_module:
                cart_module.clear_cart()
            
            # Emit order complete event
            self.shared_context['event_dispatcher']['emit']('order_complete', {
                'order_id': order_id,
                'transaction_id': transaction_id,
                'total_amount': cart_data['total']
            })
            
            return {
                'success': True,
                'order_id': order_id,
                'message': f'Order {order_id} completed successfully'
            }
        except Exception as e:
            print(f"Error completing order: {e}")
            return {'success': False, 'error': str(e)}
    
    def checkout(self, payment_method: str = "credit_card") -> dict:
        """Complete checkout flow"""
        try:
            # Step 1: Start checkout
            checkout_result = self.start_checkout(payment_method)
            if not checkout_result['success']:
                return checkout_result
            
            order_id = checkout_result['order_id']
            cart_data = checkout_result['cart_data']
            
            # Step 2: Process payment
            payment_result = self.process_payment(order_id, payment_method)
            if not payment_result['success']:
                return payment_result
            
            # Step 3: Complete order
            order_result = self.complete_order(
                order_id, 
                cart_data, 
                payment_result['transaction_id']
            )
            
            return order_result
        except Exception as e:
            print(f"Error during checkout: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_order_history(self) -> list:
        try:
            cursor = self.db_conn.cursor()
            cursor.execute('''SELECT o.order_id, o.total_amount, o.status, 
                                    o.payment_method, o.created_at,
                                    COUNT(oi.id) as item_count
                            FROM orders o
                            LEFT JOIN order_items oi ON o.order_id = oi.order_id
                            GROUP BY o.order_id
                            ORDER BY o.created_at DESC''')
            orders = cursor.fetchall()
            cursor.close()
            return orders
        except Exception as e:
            print(f"Error getting order history: {e}")
            return []
    
    def get_order_details(self, order_id: str) -> dict:
        try:
            cursor = self.db_conn.cursor()
            
            # Get order info
            cursor.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,))
            order = cursor.fetchone()
            
            if not order:
                return {'success': False, 'error': 'Order not found'}
            
            # Get order items
            cursor.execute("SELECT * FROM order_items WHERE order_id = ?", (order_id,))
            items = cursor.fetchall()
            
            cursor.close()
            
            return {
                'success': True,
                'order': order,
                'items': items
            }
        except Exception as e:
            print(f"Error getting order details: {e}")
            return {'success': False, 'error': str(e)}
    
    # Event handlers
    def on_checkout_start(self, payload, context):
        print(f"Checkout module received checkout start event: {payload}")
    
    def on_payment_process(self, payload, context):
        print(f"Checkout module received payment process event: {payload}")
    
    def on_order_complete(self, payload, context):
        print(f"Checkout module received order complete event: {payload}")
