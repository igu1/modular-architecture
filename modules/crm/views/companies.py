from modules.crm.models import Company

def list_companies(environ, start_response, crm_module):
    try:
        crm_module.log("Listing all companies", "info")
        companies = Company.all()
        return crm_module.response(start_response, {'companies': companies})
        
    except Exception as e:
        crm_module.log(f"Error listing companies: {e}", "error")
        return crm_module.response(start_response, {'error': str(e)}, '500 Internal Server Error')

def create_company(environ, start_response, crm_module):
    try:
        body = crm_module.get_body(environ)
        if not body:
            return crm_module.response(start_response, {'error': 'Invalid request'}, '400 Bad Request')
        
        name = body.get('name')
        
        if not name:
            return crm_module.response(start_response, {'error': 'Company name is required'}, '400 Bad Request')
        
        company_data = {
            'name': name,
            'industry': body.get('industry'),
            'website': body.get('website'),
            'phone': body.get('phone'),
            'email': body.get('email'),
            'address': body.get('address'),
            'city': body.get('city'),
            'state': body.get('state'),
            'country': body.get('country')
        }
        
        company = Company.create(**company_data)
        crm_module.log(f"Company created: {company['name']}", "info")
        
        crm_module.emit_event('company_created', {
            'company_id': company['id'],
            'name': company['name']
        })
        
        return crm_module.response(start_response, {'success': True, 'company': company})
        
    except Exception as e:
        crm_module.log(f"Error creating company: {e}", "error")
        return crm_module.response(start_response, {'error': str(e)}, '500 Internal Server Error')

def get_company(environ, start_response, crm_module):
    try:
        route_params = environ.get('ROUTE_PARAMS', {})
        company_id = route_params.get('id')
        
        if not company_id:
            return crm_module.response(start_response, {'error': 'Company ID is required'}, '400 Bad Request')
        
        company = Company.get(id=company_id)
        if not company:
            return crm_module.response(start_response, {'error': 'Company not found'}, '404 Not Found')
        
        return crm_module.response(start_response, {'company': company})
        
    except Exception as e:
        crm_module.log(f"Error getting company: {e}", "error")
        return crm_module.response(start_response, {'error': str(e)}, '500 Internal Server Error')

def update_company(environ, start_response, crm_module):
    try:
        route_params = environ.get('ROUTE_PARAMS', {})
        company_id = route_params.get('id')
        
        if not company_id:
            return crm_module.response(start_response, {'error': 'Company ID is required'}, '400 Bad Request')
        
        body = crm_module.get_body(environ)
        if not body:
            return crm_module.response(start_response, {'error': 'Invalid request'}, '400 Bad Request')
        
        update_data = {}
        for field in ['name', 'industry', 'website', 'phone', 'email', 'address', 'city', 'state', 'country', 'is_active']:
            if field in body:
                update_data[field] = body[field]
        
        company = Company.update_record(company_id, **update_data)
        if not company:
            return crm_module.response(start_response, {'error': 'Company not found'}, '404 Not Found')
        
        crm_module.log(f"Company updated: {company['name']}", "info")
        
        crm_module.emit_event('company_updated', {
            'company_id': company['id'],
            'name': company['name']
        })
        
        return crm_module.response(start_response, {'success': True, 'company': company})
        
    except Exception as e:
        crm_module.log(f"Error updating company: {e}", "error")
        return crm_module.response(start_response, {'error': str(e)}, '500 Internal Server Error')

def delete_company(environ, start_response, crm_module):
    try:
        route_params = environ.get('ROUTE_PARAMS', {})
        company_id = route_params.get('id')
        
        if not company_id:
            return crm_module.response(start_response, {'error': 'Company ID is required'}, '400 Bad Request')
        
        success = Company.delete_record(company_id)
        if not success:
            return crm_module.response(start_response, {'error': 'Company not found'}, '404 Not Found')
        
        crm_module.log(f"Company deleted: {company_id}", "info")
        
        crm_module.emit_event('company_deleted', {'company_id': company_id})
        
        return crm_module.response(start_response, {'success': True})
        
    except Exception as e:
        crm_module.log(f"Error deleting company: {e}", "error")
        return crm_module.response(start_response, {'error': str(e)}, '500 Internal Server Error')
