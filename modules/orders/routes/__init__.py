routes = [
    ('/api/orders', 'GET', 'modules.orders.views.orders.list_orders'),
    ('/api/orders', 'POST', 'modules.orders.views.orders.create_order'),
    ('/api/orders/<id>', 'GET', 'modules.orders.views.orders.get_order'),
    ('/api/orders/<id>', 'PUT', 'modules.orders.views.orders.update_order'),
    ('/api/orders/<id>', 'DELETE', 'modules.orders.views.orders.delete_order'),
]
