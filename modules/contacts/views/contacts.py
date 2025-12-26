from modules.contacts.models import Contact

def list_contacts(environ, start_response, contacts_module):
    try:
        contacts_module.log("Listing all contacts", "info")
        contacts = Contact.all()
        return contacts_module.response(start_response, {'contacts': contacts})
        
    except Exception as e:
        contacts_module.log(f"Error listing contacts: {e}", "error")
        return contacts_module.response(start_response, {'error': str(e)}, '500 Internal Server Error')

def create_contact(environ, start_response, contacts_module):
    try:
        body = contacts_module.get_body(environ)
        if not body:
            return contacts_module.response(start_response, {'error': 'Invalid request'}, '400 Bad Request')
        
        first_name = body.get('first_name')
        last_name = body.get('last_name')
        email = body.get('email')
        
        if not all([first_name, last_name, email]):
            return contacts_module.response(start_response, {'error': 'First name, last name, and email are required'}, '400 Bad Request')
        
        contact_data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phone': body.get('phone'),
            'mobile': body.get('mobile'),
            'title': body.get('title'),
            'department': body.get('department'),
            'account_id': body.get('account_id'),
            'lead_source': body.get('lead_source'),
            'status': body.get('status', 'active'),
            'is_primary': body.get('is_primary', False),
            'address_line1': body.get('address_line1'),
            'address_line2': body.get('address_line2'),
            'city': body.get('city'),
            'state': body.get('state'),
            'postal_code': body.get('postal_code'),
            'country': body.get('country'),
            'notes': body.get('notes')
        }
        
        # Remove None values
        contact_data = {k: v for k, v in contact_data.items() if v is not None}
        
        contact = Contact.create(**contact_data)
        contacts_module.log(f"Contact created: {contact['first_name']} {contact['last_name']}", "info")
        
        contacts_module.emit_event('contact_created', {
            'contact_id': contact['id'],
            'name': f"{contact['first_name']} {contact['last_name']}",
            'email': contact['email']
        })
        
        return contacts_module.response(start_response, {'success': True, 'contact': contact})
        
    except Exception as e:
        contacts_module.log(f"Error creating contact: {e}", "error")
        return contacts_module.response(start_response, {'error': str(e)}, '500 Internal Server Error')

def get_contact(environ, start_response, contacts_module):
    try:
        route_params = environ.get('ROUTE_PARAMS', {})
        contact_id = route_params.get('id')
        
        if not contact_id:
            return contacts_module.response(start_response, {'error': 'Contact ID is required'}, '400 Bad Request')
        
        contact = Contact.get(id=contact_id)
        if not contact:
            return contacts_module.response(start_response, {'error': 'Contact not found'}, '404 Not Found')
        
        return contacts_module.response(start_response, {'contact': contact})
        
    except Exception as e:
        contacts_module.log(f"Error getting contact: {e}", "error")
        return contacts_module.response(start_response, {'error': str(e)}, '500 Internal Server Error')

def update_contact(environ, start_response, contacts_module):
    try:
        route_params = environ.get('ROUTE_PARAMS', {})
        contact_id = route_params.get('id')
        
        if not contact_id:
            return contacts_module.response(start_response, {'error': 'Contact ID is required'}, '400 Bad Request')
        
        body = contacts_module.get_body(environ)
        if not body:
            return contacts_module.response(start_response, {'error': 'Invalid request'}, '400 Bad Request')
        
        # Remove None values
        update_data = {k: v for k, v in body.items() if v is not None}
        
        contact = Contact.update_record(contact_id, **update_data)
        if not contact:
            return contacts_module.response(start_response, {'error': 'Contact not found'}, '404 Not Found')
        
        contacts_module.log(f"Contact updated: {contact['first_name']} {contact['last_name']}", "info")
        
        contacts_module.emit_event('contact_updated', {
            'contact_id': contact['id'],
            'name': f"{contact['first_name']} {contact['last_name']}"
        })
        
        return contacts_module.response(start_response, {'success': True, 'contact': serialize_contact(contact)})
        
    except Exception as e:
        contacts_module.log(f"Error updating contact: {e}", "error")
        return contacts_module.response(start_response, {'error': str(e)}, '500 Internal Server Error')

def delete_contact(environ, start_response, contacts_module):
    try:
        route_params = environ.get('ROUTE_PARAMS', {})
        contact_id = route_params.get('id')
        
        if not contact_id:
            return contacts_module.response(start_response, {'error': 'Contact ID is required'}, '400 Bad Request')
        
        success = Contact.delete_record(contact_id)
        if not success:
            return contacts_module.response(start_response, {'error': 'Contact not found'}, '404 Not Found')
        
        contacts_module.emit_event('contact_deleted', {'contact_id': contact_id})
        
        return contacts_module.response(start_response, {'success': True})
        
    except Exception as e:
        contacts_module.log(f"Error deleting contact: {e}", "error")
        return contacts_module.response(start_response, {'error': str(e)}, '500 Internal Server Error')
