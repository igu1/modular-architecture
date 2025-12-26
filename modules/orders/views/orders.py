def list_orders(environ, start_response, module):
    session = module.get_db_session()()
    order_service = module.env.get_service('orders_order_service')
    orders = order_service.list_orders(session)
    return module.response(start_response, {'orders': [o.__dict__ for o in orders]})

def create_order(environ, start_response, module):
    body = module.get_body(environ)
    session = module.get_db_session()()
    order_service = module.env.get_service('orders_order_service')
    order = order_service.create_order(session, body)
    module.emit_event('order_created', {'order_id': order.id})
    return module.response(start_response, {'order': order.__dict__}, '201 Created')

def get_order(environ, start_response, module):
    order_id = environ['ROUTE_PARAMS']['id']
    session = module.get_db_session()()
    order_service = module.env.get_service('orders_order_service')
    order = order_service.get_order(session, order_id)
    if order:
        return module.response(start_response, {'order': order.__dict__})
    return module.response(start_response, {'error': 'Order not found'}, '404 Not Found')

def update_order(environ, start_response, module):
    order_id = environ['ROUTE_PARAMS']['id']
    body = module.get_body(environ)
    session = module.get_db_session()()
    order_service = module.env.get_service('orders_order_service')
    order = order_service.update_order(session, order_id, body)
    if order:
        module.emit_event('order_updated', {'order_id': order.id})
        return module.response(start_response, {'order': order.__dict__})
    return module.response(start_response, {'error': 'Order not found'}, '404 Not Found')

def delete_order(environ, start_response, module):
    order_id = environ['ROUTE_PARAMS']['id']
    session = module.get_db_session()()
    order_service = module.env.get_service('orders_order_service')
    if order_service.delete_order(session, order_id):
        module.emit_event('order_deleted', {'order_id': order_id})
        return module.response(start_response, {'message': 'Order deleted'})
    return module.response(start_response, {'error': 'Order not found'}, '404 Not Found')
