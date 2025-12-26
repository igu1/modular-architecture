def list_products(environ, start_response, module):
    session = module.get_db_session()()
    product_service = module.env.get_service('products_product_service')
    products = product_service.list_products(session)
    return module.response(start_response, {'products': [p.__dict__ for p in products]})

def create_product(environ, start_response, module):
    body = module.get_body(environ)
    session = module.get_db_session()()
    product_service = module.env.get_service('products_product_service')
    product = product_service.create_product(session, body)
    module.emit_event('product_created', {'product_id': product.id})
    return module.response(start_response, {'product': product.__dict__}, '201 Created')

def get_product(environ, start_response, module):
    product_id = environ['ROUTE_PARAMS']['id']
    session = module.get_db_session()()
    product_service = module.env.get_service('products_product_service')
    product = product_service.get_product(session, product_id)
    if product:
        return module.response(start_response, {'product': product.__dict__})
    return module.response(start_response, {'error': 'Product not found'}, '404 Not Found')

def update_product(environ, start_response, module):
    product_id = environ['ROUTE_PARAMS']['id']
    body = module.get_body(environ)
    session = module.get_db_session()()
    product_service = module.env.get_service('products_product_service')
    product = product_service.update_product(session, product_id, body)
    if product:
        module.emit_event('product_updated', {'product_id': product.id})
        return module.response(start_response, {'product': product.__dict__})
    return module.response(start_response, {'error': 'Product not found'}, '404 Not Found')

def delete_product(environ, start_response, module):
    product_id = environ['ROUTE_PARAMS']['id']
    session = module.get_db_session()()
    product_service = module.env.get_service('products_product_service')
    if product_service.delete_product(session, product_id):
        module.emit_event('product_deleted', {'product_id': product_id})
        return module.response(start_response, {'message': 'Product deleted'})
    return module.response(start_response, {'error': 'Product not found'}, '404 Not Found')
