class ProductService:
    
    def __init__(self):
        self.name = "product_service"
    
    def create_product(self, session, product_data):
        from modules.products.models import Product
        product = Product(**product_data)
        session.add(product)
        session.commit()
        return product
    
    def get_product(self, session, product_id):
        from modules.products.models import Product
        return session.query(Product).filter(Product.id == product_id).first()
    
    def update_product(self, session, product_id, product_data):
        from modules.products.models import Product
        product = session.query(Product).filter(Product.id == product_id).first()
        if product:
            for key, value in product_data.items():
                setattr(product, key, value)
            session.commit()
        return product
    
    def delete_product(self, session, product_id):
        from modules.products.models import Product
        product = session.query(Product).filter(Product.id == product_id).first()
        if product:
            session.delete(product)
            session.commit()
            return True
        return False
    
    def list_products(self, session, filters=None):
        from modules.products.models import Product
        query = session.query(Product)
        if filters:
            for key, value in filters.items():
                query = query.filter(getattr(Product, key) == value)
        return query.all()
