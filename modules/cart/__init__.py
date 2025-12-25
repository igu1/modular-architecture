from .cart import Cart

def initialize(db_conn, shared_context):
    return Cart().initialize(db_conn, shared_context)

def deinitialize():
    return Cart().deinitialize()
