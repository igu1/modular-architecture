routes = [
    ('/customers', 'GET', 'modules.customers.views.customers.list_customers'),
    ('/customers', 'POST', 'modules.customers.views.customers.create_customer'),
    ('/customers/<id>', 'GET', 'modules.customers.views.customers.get_customer'),
    ('/customers/<id>', 'PUT', 'modules.customers.views.customers.update_customer'),
    ('/customers/<id>', 'DELETE', 'modules.customers.views.customers.delete_customer'),
]
