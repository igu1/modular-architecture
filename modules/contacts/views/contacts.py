def serialize_contact(contact):
    """Convert SQLAlchemy Contact object to dictionary"""
    return {
        'id': contact.id,
        'first_name': contact.first_name,
        'last_name': contact.last_name,
        'email': contact.email,
        'phone': contact.phone,
        'mobile': contact.mobile,
        'title': contact.title,
        'department': contact.department,
        'account_id': contact.account_id,
        'lead_source': contact.lead_source,
        'status': contact.status,
        'is_primary': contact.is_primary,
        'address_line1': contact.address_line1,
        'address_line2': contact.address_line2,
        'city': contact.city,
        'state': contact.state,
        'postal_code': contact.postal_code,
        'country': contact.country,
        'notes': contact.notes,
        'created_by': contact.created_by,
        'assigned_to': contact.assigned_to
    }

def list_contacts(environ, start_response, module):
    session = module.get_db_session()()
    contact_service = module.env.get_service('contacts_contact_service')
    contacts = contact_service.list_contacts(session)
    return module.response(start_response, {'contacts': [serialize_contact(c) for c in contacts]})

def create_contact(environ, start_response, module):
    body = module.get_body(environ)
    session = module.get_db_session()()
    contact_service = module.env.get_service('contacts_contact_service')
    contact = contact_service.create_contact(session, body)
    module.emit_event('contact_created', {'contact_id': contact.id})
    return module.response(start_response, {'contact': serialize_contact(contact)}, '201 Created')

def get_contact(environ, start_response, module):
    contact_id = environ['ROUTE_PARAMS']['id']
    session = module.get_db_session()()
    contact_service = module.env.get_service('contacts_contact_service')
    contact = contact_service.get_contact(session, contact_id)
    if contact:
        return module.response(start_response, {'contact': serialize_contact(contact)})
    return module.response(start_response, {'error': 'Contact not found'}, '404 Not Found')

def update_contact(environ, start_response, module):
    contact_id = environ['ROUTE_PARAMS']['id']
    body = module.get_body(environ)
    session = module.get_db_session()()
    contact_service = module.env.get_service('contacts_contact_service')
    contact = contact_service.update_contact(session, contact_id, body)
    if contact:
        module.emit_event('contact_updated', {'contact_id': contact.id})
        return module.response(start_response, {'contact': serialize_contact(contact)})
    return module.response(start_response, {'error': 'Contact not found'}, '404 Not Found')

def delete_contact(environ, start_response, module):
    contact_id = environ['ROUTE_PARAMS']['id']
    session = module.get_db_session()()
    contact_service = module.env.get_service('contacts_contact_service')
    success = contact_service.delete_contact(session, contact_id)
    if success:
        module.emit_event('contact_deleted', {'contact_id': contact_id})
        return module.response(start_response, {'success': True})
    return module.response(start_response, {'error': 'Contact not found'}, '404 Not Found')
