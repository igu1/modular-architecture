from modules.leads.models import Lead, LeadStatus

def list_leads(environ, start_response, leads_module):
    try:
        auth_service = leads_module.env.get_service('auth_auth_service')
        user = auth_service.require_auth(environ, start_response, leads_module)
        if not user:
            return leads_module.response(start_response, {'error': 'Authentication required'}, '401 Unauthorized')
        
        leads_module.log("Listing all leads", "info")
        leads = Lead.all()
        return leads_module.response(start_response, {'leads': leads})
        
    except Exception as e:
        leads_module.log(f"Error listing leads: {e}", "error")
        return leads_module.response(start_response, {'error': str(e)}, '500 Internal Server Error')

def create_lead(environ, start_response, leads_module):
    try:
        auth_service = leads_module.env.get_service('auth_auth_service')
        user = auth_service.require_auth(environ, start_response, leads_module)
        if not user:
            return leads_module.response(start_response, {'error': 'Authentication required'}, '401 Unauthorized')
        
        body = leads_module.get_body(environ)
        if not body:
            return leads_module.response(start_response, {'error': 'Invalid request'}, '400 Bad Request')
        
        name = body.get('name')
        email = body.get('email')
        company_id = body.get('company_id')
        
        if not all([name, email, company_id]):
            return leads_module.response(start_response, {'error': 'Name, email, and company_id are required'}, '400 Bad Request')
        
        lead_data = {
            'company_id': company_id,
            'name': name,
            'email': email,
            'phone': body.get('phone'),
            'company': body.get('company'),
            'source': body.get('source'),
            'notes': body.get('notes'),
            'assigned_to': user['id']
        }
        
        lead = Lead.create(**lead_data)
        leads_module.log(f"Lead created: {lead['name']} ({lead['email']})", "info")
        
        leads_module.emit_event('lead_created', {
            'lead_id': lead['id'],
            'company_id': lead['company_id'],
            'name': lead['name'],
            'email': lead['email']
        })
        
        return leads_module.response(start_response, {'success': True, 'lead': lead})
        
    except Exception as e:
        leads_module.log(f"Error creating lead: {e}", "error")
        return leads_module.response(start_response, {'error': str(e)}, '500 Internal Server Error')

def get_lead(environ, start_response, leads_module):
    try:
        auth_service = leads_module.env.get_service('auth_auth_service')
        user = auth_service.require_auth(environ, start_response, leads_module)
        if not user:
            return leads_module.response(start_response, {'error': 'Authentication required'}, '401 Unauthorized')
        
        route_params = environ.get('ROUTE_PARAMS', {})
        lead_id = route_params.get('id')
        
        if not lead_id:
            return leads_module.response(start_response, {'error': 'Lead ID is required'}, '400 Bad Request')
        
        lead = Lead.get(id=lead_id)
        if not lead:
            return leads_module.response(start_response, {'error': 'Lead not found'}, '404 Not Found')
        
        return leads_module.response(start_response, {'lead': lead})
        
    except Exception as e:
        leads_module.log(f"Error getting lead: {e}", "error")
        return leads_module.response(start_response, {'error': str(e)}, '500 Internal Server Error')

def update_lead(environ, start_response, leads_module):
    try:
        auth_service = leads_module.env.get_service('auth_auth_service')
        user = auth_service.require_auth(environ, start_response, leads_module)
        if not user:
            return leads_module.response(start_response, {'error': 'Authentication required'}, '401 Unauthorized')
        
        route_params = environ.get('ROUTE_PARAMS', {})
        lead_id = route_params.get('id')
        
        if not lead_id:
            return leads_module.response(start_response, {'error': 'Lead ID is required'}, '400 Bad Request')
        
        body = leads_module.get_body(environ)
        if not body:
            return leads_module.response(start_response, {'error': 'Invalid request'}, '400 Bad Request')
        
        update_data = {}
        for field in ['name', 'email', 'phone', 'company', 'source', 'notes', 'status']:
            if field in body:
                if field == 'status':
                    update_data[field] = LeadStatus[body[field].upper()]
                else:
                    update_data[field] = body[field]
        
        lead = Lead.update_record(lead_id, **update_data)
        if not lead:
            return leads_module.response(start_response, {'error': 'Lead not found'}, '404 Not Found')
        
        leads_module.log(f"Lead updated: {lead['name']}", "info")
        
        leads_module.emit_event('lead_updated', {
            'lead_id': lead['id'],
            'name': lead['name']
        })
        
        return leads_module.response(start_response, {'success': True, 'lead': lead})
        
    except Exception as e:
        leads_module.log(f"Error updating lead: {e}", "error")
        return leads_module.response(start_response, {'error': str(e)}, '500 Internal Server Error')

def delete_lead(environ, start_response, leads_module):
    try:
        auth_service = leads_module.env.get_service('auth_auth_service')
        user = auth_service.require_auth(environ, start_response, leads_module)
        if not user:
            return leads_module.response(start_response, {'error': 'Authentication required'}, '401 Unauthorized')
        
        route_params = environ.get('ROUTE_PARAMS', {})
        lead_id = route_params.get('id')
        
        if not lead_id:
            return leads_module.response(start_response, {'error': 'Lead ID is required'}, '400 Bad Request')
        
        success = Lead.delete_record(lead_id)
        if not success:
            return leads_module.response(start_response, {'error': 'Lead not found'}, '404 Not Found')
        
        leads_module.log(f"Lead deleted: {lead_id}", "info")
        
        leads_module.emit_event('lead_deleted', {'lead_id': lead_id})
        
        return leads_module.response(start_response, {'success': True})
        
    except Exception as e:
        leads_module.log(f"Error deleting lead: {e}", "error")
        return leads_module.response(start_response, {'error': str(e)}, '500 Internal Server Error')

def convert_lead(environ, start_response, leads_module):
    try:
        auth_service = leads_module.env.get_service('auth_auth_service')
        user = auth_service.require_auth(environ, start_response, leads_module)
        if not user:
            return leads_module.response(start_response, {'error': 'Authentication required'}, '401 Unauthorized')
        
        route_params = environ.get('ROUTE_PARAMS', {})
        lead_id = route_params.get('id')
        
        if not lead_id:
            return leads_module.response(start_response, {'error': 'Lead ID is required'}, '400 Bad Request')
        
        lead = Lead.update_record(lead_id, status=LeadStatus.CONVERTED)
        if not lead:
            return leads_module.response(start_response, {'error': 'Lead not found'}, '404 Not Found')
        
        leads_module.log(f"Lead converted: {lead['name']}", "info")
        
        leads_module.emit_event('lead_converted', {
            'lead_id': lead['id'],
            'name': lead['name'],
            'email': lead['email']
        })
        
        return leads_module.response(start_response, {'success': True, 'lead': lead})
        
    except Exception as e:
        leads_module.log(f"Error converting lead: {e}", "error")
        return leads_module.response(start_response, {'error': str(e)}, '500 Internal Server Error')
