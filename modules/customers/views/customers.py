from modules.customers.models import Customer

def list_customers(environ, start_response, customers_module):
    try:
        customers_module.log("Listing all customers", "info")
        customers = Customer.all()
        return customers_module.response(start_response, {'customers': customers})
        
    except Exception as e:
        customers_module.log(f"Error listing customers: {e}", "error")
        return customers_module.response(start_response, {'error': str(e)}, '500 Internal Server Error')

def create_customer(environ, start_response, customers_module):
    try:
        body = customers_module.get_body(environ)
        if not body:
            return customers_module.response(start_response, {'error': 'Invalid request'}, '400 Bad Request')
        
        name = body.get('name')
        email = body.get('email')
        company_id = body.get('company_id')
        
        if not all([name, email, company_id]):
            return customers_module.response(start_response, {'error': 'Name, email, and company_id are required'}, '400 Bad Request')
        
        if Customer.get(email=email):
            return customers_module.response(start_response, {'error': 'Customer with this email already exists'}, '400 Bad Request')
        
        customer_data = {
            'company_id': company_id,
            'lead_id': body.get('lead_id'),
            'name': name,
            'email': email,
            'phone': body.get('phone'),
            'company': body.get('company'),
            'address': body.get('address'),
            'city': body.get('city'),
            'country': body.get('country'),
            'notes': body.get('notes')
        }
        
        customer = Customer.create(**customer_data)
        customers_module.log(f"Customer created: {customer['name']} ({customer['email']})", "info")
        
        customers_module.emit_event('customer_created', {
            'customer_id': customer['id'],
            'company_id': customer['company_id'],
            'name': customer['name'],
            'email': customer['email']
        })
        
        return customers_module.response(start_response, {'success': True, 'customer': customer})
        
    except Exception as e:
        customers_module.log(f"Error creating customer: {e}", "error")
        return customers_module.response(start_response, {'error': str(e)}, '500 Internal Server Error')

def get_customer(environ, start_response, customers_module):
    try:
        route_params = environ.get('ROUTE_PARAMS', {})
        customer_id = route_params.get('id')
        
        if not customer_id:
            return customers_module.response(start_response, {'error': 'Customer ID is required'}, '400 Bad Request')
        
        customer = Customer.get(id=customer_id)
        if not customer:
            return customers_module.response(start_response, {'error': 'Customer not found'}, '404 Not Found')
        
        return customers_module.response(start_response, {'customer': customer})
        
    except Exception as e:
        customers_module.log(f"Error getting customer: {e}", "error")
        return customers_module.response(start_response, {'error': str(e)}, '500 Internal Server Error')

def update_customer(environ, start_response, customers_module):
    try:
        route_params = environ.get('ROUTE_PARAMS', {})
        customer_id = route_params.get('id')
        
        if not customer_id:
            return customers_module.response(start_response, {'error': 'Customer ID is required'}, '400 Bad Request')
        
        body = customers_module.get_body(environ)
        if not body:
            return customers_module.response(start_response, {'error': 'Invalid request'}, '400 Bad Request')
        
        update_data = {}
        for field in ['name', 'email', 'phone', 'company', 'address', 'city', 'country', 'notes', 'is_active']:
            if field in body:
                update_data[field] = body[field]
        
        customer = Customer.update_record(customer_id, **update_data)
        if not customer:
            return customers_module.response(start_response, {'error': 'Customer not found'}, '404 Not Found')
        
        customers_module.log(f"Customer updated: {customer['name']}", "info")
        
        customers_module.emit_event('customer_updated', {
            'customer_id': customer['id'],
            'name': customer['name']
        })
        
        return customers_module.response(start_response, {'success': True, 'customer': customer})
        
    except Exception as e:
        customers_module.log(f"Error updating customer: {e}", "error")
        return customers_module.response(start_response, {'error': str(e)}, '500 Internal Server Error')

def delete_customer(environ, start_response, customers_module):
    try:
        route_params = environ.get('ROUTE_PARAMS', {})
        customer_id = route_params.get('id')
        
        if not customer_id:
            return customers_module.response(start_response, {'error': 'Customer ID is required'}, '400 Bad Request')
        
        success = Customer.delete_record(customer_id)
        if not success:
            return customers_module.response(start_response, {'error': 'Customer not found'}, '404 Not Found')
        
        customers_module.log(f"Customer deleted: {customer_id}", "info")
        
        customers_module.emit_event('customer_deleted', {'customer_id': customer_id})
        
        return customers_module.response(start_response, {'success': True})
        
    except Exception as e:
        customers_module.log(f"Error deleting customer: {e}", "error")
        return customers_module.response(start_response, {'error': str(e)}, '500 Internal Server Error')
