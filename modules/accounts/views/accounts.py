from modules.accounts.models import Account

def list_accounts(environ, start_response, accounts_module):
    try:
        accounts_module.log("Listing all accounts", "info")
        accounts = Account.all()
        return accounts_module.response(start_response, {'accounts': accounts})
        
    except Exception as e:
        accounts_module.log(f"Error listing accounts: {e}", "error")
        return accounts_module.response(start_response, {'error': str(e)}, '500 Internal Server Error')

def create_account(environ, start_response, accounts_module):
    try:
        body = accounts_module.get_body(environ)
        if not body:
            return accounts_module.response(start_response, {'error': 'Invalid request'}, '400 Bad Request')
        
        name = body.get('name')
        
        if not name:
            return accounts_module.response(start_response, {'error': 'Account name is required'}, '400 Bad Request')
        
        account_data = {
            'name': name,
            'account_number': body.get('account_number'),
            'account_type': body.get('account_type'),
            'industry': body.get('industry'),
            'website': body.get('website'),
            'phone': body.get('phone'),
            'annual_revenue': body.get('annual_revenue'),
            'number_of_employees': body.get('number_of_employees'),
            'status': body.get('status', 'active'),
            'description': body.get('description'),
            'notes': body.get('notes')
        }
        
        # Remove None values
        account_data = {k: v for k, v in account_data.items() if v is not None}
        
        account = Account.create(**account_data)
        accounts_module.log(f"Account created: {account['name']}", "info")
        
        accounts_module.emit_event('account_created', {
            'account_id': account['id'],
            'name': account['name']
        })
        
        return accounts_module.response(start_response, {'success': True, 'account': account})
        
    except Exception as e:
        accounts_module.log(f"Error creating account: {e}", "error")
        return accounts_module.response(start_response, {'error': str(e)}, '500 Internal Server Error')

def get_account(environ, start_response, accounts_module):
    try:
        route_params = environ.get('ROUTE_PARAMS', {})
        account_id = route_params.get('id')
        
        if not account_id:
            return accounts_module.response(start_response, {'error': 'Account ID is required'}, '400 Bad Request')
        
        account = Account.get(id=account_id)
        if not account:
            return accounts_module.response(start_response, {'error': 'Account not found'}, '404 Not Found')
        
        return accounts_module.response(start_response, {'account': account})
        
    except Exception as e:
        accounts_module.log(f"Error getting account: {e}", "error")
        return accounts_module.response(start_response, {'error': str(e)}, '500 Internal Server Error')

def update_account(environ, start_response, accounts_module):
    try:
        route_params = environ.get('ROUTE_PARAMS', {})
        account_id = route_params.get('id')
        
        if not account_id:
            return accounts_module.response(start_response, {'error': 'Account ID is required'}, '400 Bad Request')
        
        body = accounts_module.get_body(environ)
        if not body:
            return accounts_module.response(start_response, {'error': 'Invalid request'}, '400 Bad Request')
        
        # Remove None values
        update_data = {k: v for k, v in body.items() if v is not None}
        
        account = Account.update_record(account_id, **update_data)
        if not account:
            return accounts_module.response(start_response, {'error': 'Account not found'}, '404 Not Found')
        
        accounts_module.log(f"Account updated: {account['name']}", "info")
        
        accounts_module.emit_event('account_updated', {
            'account_id': account['id'],
            'name': account['name']
        })
        
        return accounts_module.response(start_response, {'success': True, 'account': account})
        
    except Exception as e:
        accounts_module.log(f"Error updating account: {e}", "error")
        return accounts_module.response(start_response, {'error': str(e)}, '500 Internal Server Error')

def delete_account(environ, start_response, accounts_module):
    try:
        route_params = environ.get('ROUTE_PARAMS', {})
        account_id = route_params.get('id')
        
        if not account_id:
            return accounts_module.response(start_response, {'error': 'Account ID is required'}, '400 Bad Request')
        
        success = Account.delete_record(account_id)
        if not success:
            return accounts_module.response(start_response, {'error': 'Account not found'}, '404 Not Found')
        
        accounts_module.emit_event('account_deleted', {'account_id': account_id})
        
        return accounts_module.response(start_response, {'success': True})
        
    except Exception as e:
        accounts_module.log(f"Error deleting account: {e}", "error")
        return accounts_module.response(start_response, {'error': str(e)}, '500 Internal Server Error')
