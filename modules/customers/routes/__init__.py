routes = [
    ('/api/customers', 'GET', 'modules.customers.views.customers.list_customers'),
    ('/api/customers', 'POST', 'modules.customers.views.customers.create_customer'),
    ('/api/customers/<id>', 'GET', 'modules.customers.views.customers.get_customer'),
    ('/api/customers/<id>', 'PUT', 'modules.customers.views.customers.update_customer'),
    ('/api/customers/<id>', 'DELETE', 'modules.customers.views.customers.delete_customer'),
]
