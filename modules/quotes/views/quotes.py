def list_quotes(environ, start_response, module):
    session = module.get_db_session()()
    quote_service = module.env.get_service('quotes_quote_service')
    quotes = quote_service.list_quotes(session)
    return module.response(start_response, {'quotes': [q.__dict__ for q in quotes]})

def create_quote(environ, start_response, module):
    body = module.get_body(environ)
    session = module.get_db_session()()
    quote_service = module.env.get_service('quotes_quote_service')
    quote = quote_service.create_quote(session, body)
    module.emit_event('quote_created', {'quote_id': quote.id})
    return module.response(start_response, {'quote': quote.__dict__}, '201 Created')

def get_quote(environ, start_response, module):
    quote_id = environ['ROUTE_PARAMS']['id']
    session = module.get_db_session()()
    quote_service = module.env.get_service('quotes_quote_service')
    quote = quote_service.get_quote(session, quote_id)
    if quote:
        return module.response(start_response, {'quote': quote.__dict__})
    return module.response(start_response, {'error': 'Quote not found'}, '404 Not Found')

def update_quote(environ, start_response, module):
    quote_id = environ['ROUTE_PARAMS']['id']
    body = module.get_body(environ)
    session = module.get_db_session()()
    quote_service = module.env.get_service('quotes_quote_service')
    quote = quote_service.update_quote(session, quote_id, body)
    if quote:
        module.emit_event('quote_updated', {'quote_id': quote.id})
        return module.response(start_response, {'quote': quote.__dict__})
    return module.response(start_response, {'error': 'Quote not found'}, '404 Not Found')

def delete_quote(environ, start_response, module):
    quote_id = environ['ROUTE_PARAMS']['id']
    session = module.get_db_session()()
    quote_service = module.env.get_service('quotes_quote_service')
    if quote_service.delete_quote(session, quote_id):
        module.emit_event('quote_deleted', {'quote_id': quote_id})
        return module.response(start_response, {'message': 'Quote deleted'})
    return module.response(start_response, {'error': 'Quote not found'}, '404 Not Found')
