def list_tickets(environ, start_response, module):
    session = module.get_db_session()()
    ticket_service = module.env.get_service('tickets_ticket_service')
    tickets = ticket_service.list_tickets(session)
    return module.response(start_response, {'tickets': [t.__dict__ for t in tickets]})

def create_ticket(environ, start_response, module):
    body = module.get_body(environ)
    session = module.get_db_session()()
    ticket_service = module.env.get_service('tickets_ticket_service')
    ticket = ticket_service.create_ticket(session, body)
    module.emit_event('ticket_created', {'ticket_id': ticket.id})
    return module.response(start_response, {'ticket': ticket.__dict__}, '201 Created')

def get_ticket(environ, start_response, module):
    ticket_id = environ['ROUTE_PARAMS']['id']
    session = module.get_db_session()()
    ticket_service = module.env.get_service('tickets_ticket_service')
    ticket = ticket_service.get_ticket(session, ticket_id)
    if ticket:
        return module.response(start_response, {'ticket': ticket.__dict__})
    return module.response(start_response, {'error': 'Ticket not found'}, '404 Not Found')

def update_ticket(environ, start_response, module):
    ticket_id = environ['ROUTE_PARAMS']['id']
    body = module.get_body(environ)
    session = module.get_db_session()()
    ticket_service = module.env.get_service('tickets_ticket_service')
    ticket = ticket_service.update_ticket(session, ticket_id, body)
    if ticket:
        module.emit_event('ticket_updated', {'ticket_id': ticket.id})
        return module.response(start_response, {'ticket': ticket.__dict__})
    return module.response(start_response, {'error': 'Ticket not found'}, '404 Not Found')

def delete_ticket(environ, start_response, module):
    ticket_id = environ['ROUTE_PARAMS']['id']
    session = module.get_db_session()()
    ticket_service = module.env.get_service('tickets_ticket_service')
    if ticket_service.delete_ticket(session, ticket_id):
        module.emit_event('ticket_deleted', {'ticket_id': ticket_id})
        return module.response(start_response, {'message': 'Ticket deleted'})
    return module.response(start_response, {'error': 'Ticket not found'}, '404 Not Found')

def add_comment(environ, start_response, module):
    ticket_id = environ['ROUTE_PARAMS']['id']
    body = module.get_body(environ)
    body['ticket_id'] = ticket_id
    session = module.get_db_session()()
    ticket_service = module.env.get_service('tickets_ticket_service')
    comment = ticket_service.add_comment(session, body)
    return module.response(start_response, {'comment': comment.__dict__}, '201 Created')
