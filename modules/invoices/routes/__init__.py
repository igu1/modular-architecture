routes = [
    ('/api/invoices', 'GET', 'modules.invoices.views.invoices.list_invoices'),
    ('/api/invoices', 'POST', 'modules.invoices.views.invoices.create_invoice'),
    ('/api/invoices/<id>', 'GET', 'modules.invoices.views.invoices.get_invoice'),
    ('/api/invoices/<id>', 'PUT', 'modules.invoices.views.invoices.update_invoice'),
    ('/api/invoices/<id>', 'DELETE', 'modules.invoices.views.invoices.delete_invoice'),
    ('/api/invoices/<id>/payments', 'POST', 'modules.invoices.views.invoices.add_payment'),
]
