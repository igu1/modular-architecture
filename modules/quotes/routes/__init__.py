routes = [
    ('/api/quotes', 'GET', 'modules.quotes.views.quotes.list_quotes'),
    ('/api/quotes', 'POST', 'modules.quotes.views.quotes.create_quote'),
    ('/api/quotes/<id>', 'GET', 'modules.quotes.views.quotes.get_quote'),
    ('/api/quotes/<id>', 'PUT', 'modules.quotes.views.quotes.update_quote'),
    ('/api/quotes/<id>', 'DELETE', 'modules.quotes.views.quotes.delete_quote'),
]
