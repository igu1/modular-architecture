routes = [
    ('/api/products', 'GET', 'modules.products.views.products.list_products'),
    ('/api/products', 'POST', 'modules.products.views.products.create_product'),
    ('/api/products/<id>', 'GET', 'modules.products.views.products.get_product'),
    ('/api/products/<id>', 'PUT', 'modules.products.views.products.update_product'),
    ('/api/products/<id>', 'DELETE', 'modules.products.views.products.delete_product'),
]
