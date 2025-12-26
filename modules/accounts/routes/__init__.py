routes = [
    ('/api/accounts', 'GET', 'modules.accounts.views.accounts.list_accounts'),
    ('/api/accounts', 'POST', 'modules.accounts.views.accounts.create_account'),
    ('/api/accounts/<id>', 'GET', 'modules.accounts.views.accounts.get_account'),
    ('/api/accounts/<id>', 'PUT', 'modules.accounts.views.accounts.update_account'),
    ('/api/accounts/<id>', 'DELETE', 'modules.accounts.views.accounts.delete_account'),
]
