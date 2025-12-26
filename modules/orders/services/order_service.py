class OrderService:
    
    def __init__(self):
        self.name = "order_service"
    
    def create_order(self, session, order_data):
        from modules.orders.models import Order
        order = Order(**order_data)
        session.add(order)
        session.commit()
        return order
    
    def get_order(self, session, order_id):
        from modules.orders.models import Order
        return session.query(Order).filter(Order.id == order_id).first()
    
    def update_order(self, session, order_id, order_data):
        from modules.orders.models import Order
        order = session.query(Order).filter(Order.id == order_id).first()
        if order:
            for key, value in order_data.items():
                setattr(order, key, value)
            session.commit()
        return order
    
    def delete_order(self, session, order_id):
        from modules.orders.models import Order
        order = session.query(Order).filter(Order.id == order_id).first()
        if order:
            session.delete(order)
            session.commit()
            return True
        return False
    
    def list_orders(self, session, filters=None):
        from modules.orders.models import Order
        query = session.query(Order)
        if filters:
            for key, value in filters.items():
                query = query.filter(getattr(Order, key) == value)
        return query.all()
