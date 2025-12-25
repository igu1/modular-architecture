from .product import Product

def initialize(db_conn, shared_context):
    return Product().initialize(db_conn, shared_context)

def deinitialize():
    return Product().deinitialize()
