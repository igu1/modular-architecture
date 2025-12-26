def list_accounts(environ, start_response, module):
    session = module.get_db_session()()
    account_service = module.env.get_service('accounts_account_service')
    accounts = account_service.list_accounts(session)
    return module.response(start_response, {'accounts': [a.__dict__ for a in accounts]})

def create_account(environ, start_response, module):
    body = module.get_body(environ)
    session = module.get_db_session()()
    account_service = module.env.get_service('accounts_account_service')
    account = account_service.create_account(session, body)
    module.emit_event('account_created', {'account_id': account.id})
    return module.response(start_response, {'account': account.__dict__}, '201 Created')

def get_account(environ, start_response, module):
    account_id = environ['ROUTE_PARAMS']['id']
    session = module.get_db_session()()
    account_service = module.env.get_service('accounts_account_service')
    account = account_service.get_account(session, account_id)
    if account:
        return module.response(start_response, {'account': account.__dict__})
    return module.response(start_response, {'error': 'Account not found'}, '404 Not Found')

def update_account(environ, start_response, module):
    account_id = environ['ROUTE_PARAMS']['id']
    body = module.get_body(environ)
    session = module.get_db_session()()
    account_service = module.env.get_service('accounts_account_service')
    account = account_service.update_account(session, account_id, body)
    if account:
        module.emit_event('account_updated', {'account_id': account.id})
        return module.response(start_response, {'account': account.__dict__})
    return module.response(start_response, {'error': 'Account not found'}, '404 Not Found')

def delete_account(environ, start_response, module):
    account_id = environ['ROUTE_PARAMS']['id']
    session = module.get_db_session()()
    account_service = module.env.get_service('accounts_account_service')
    if account_service.delete_account(session, account_id):
        module.emit_event('account_deleted', {'account_id': account_id})
        return module.response(start_response, {'message': 'Account deleted'})
    return module.response(start_response, {'error': 'Account not found'}, '404 Not Found')
