def list_contacts(environ, start_response, module):
    session = module.get_db_session()()
    contact_service = module.env.get_service('contacts_contact_service')
    contacts = contact_service.list_contacts(session)
    return module.response(start_response, {'contacts': [c.__dict__ for c in contacts]})

def create_contact(environ, start_response, module):
    body = module.get_body(environ)
    session = module.get_db_session()()
    contact_service = module.env.get_service('contacts_contact_service')
    contact = contact_service.create_contact(session, body)
    module.emit_event('contact_created', {'contact_id': contact.id})
    return module.response(start_response, {'contact': contact.__dict__}, '201 Created')

def get_contact(environ, start_response, module):
    contact_id = environ['ROUTE_PARAMS']['id']
    session = module.get_db_session()()
    contact_service = module.env.get_service('contacts_contact_service')
    contact = contact_service.get_contact(session, contact_id)
    if contact:
        return module.response(start_response, {'contact': contact.__dict__})
    return module.response(start_response, {'error': 'Contact not found'}, '404 Not Found')

def update_contact(environ, start_response, module):
    contact_id = environ['ROUTE_PARAMS']['id']
    body = module.get_body(environ)
    session = module.get_db_session()()
    contact_service = module.env.get_service('contacts_contact_service')
    contact = contact_service.update_contact(session, contact_id, body)
    if contact:
        module.emit_event('contact_updated', {'contact_id': contact.id})
        return module.response(start_response, {'contact': contact.__dict__})
    return module.response(start_response, {'error': 'Contact not found'}, '404 Not Found')

def delete_contact(environ, start_response, module):
    contact_id = environ['ROUTE_PARAMS']['id']
    session = module.get_db_session()()
    contact_service = module.env.get_service('contacts_contact_service')
    if contact_service.delete_contact(session, contact_id):
        module.emit_event('contact_deleted', {'contact_id': contact_id})
        return module.response(start_response, {'message': 'Contact deleted'})
    return module.response(start_response, {'error': 'Contact not found'}, '404 Not Found')
