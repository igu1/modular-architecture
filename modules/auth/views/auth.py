import json
from datetime import datetime, timedelta
from modules.auth.models import User, Session

def login(environ, start_response, auth_module): 
    try:
        auth_service = auth_module.env.get_service('auth_auth_service')
        body = auth_module.get_body(environ)
        if not body:
            return auth_module.response(start_response, {'error': 'Invalid request'})
        
        username = body.get('username')
        password = body.get('password')
        
        if not username or not password:
            return auth_module.response(start_response, {'error': 'Username and password required'})
        
        user_dict = User.get(username=username)
        if not user_dict or not user_dict.get('is_active'):
            return auth_module.response(start_response, {'error': 'Invalid credentials'})
        
        password_hash = auth_service.hash_password(password)
        if user_dict['password_hash'] != password_hash:
            return auth_module.response(start_response, {'error': 'Invalid credentials'})
        
        session_token = auth_service.generate_session_token()
        expires_at = datetime.utcnow() + timedelta(hours=24)
        
        session_dict = Session.create(
            user_id=user_dict['id'],
            session_token=session_token,
            expires_at=expires_at
        )
        
        User.update_record(user_dict['id'], last_login=datetime.utcnow())
        
        return auth_module.response(start_response, {
            'success': True,
            'session_token': session_token,
            'user': {
                'id': user_dict['id'],
                'username': user_dict['username'],
                'email': user_dict['email']
            }
        })
        
    except Exception as e:
        return auth_module.response(start_response, {'error': str(e)})

def logout(environ, start_response, auth_module): 
    try:
        auth_service = auth_module.env.get_service('auth_auth_service')
        session_token = auth_service.get_session_token(environ)
        if session_token:
            session_dict = Session.get(session_token=session_token)
            if session_dict:
                Session.delete_record(session_dict['id'])
        
        return auth_module.response(start_response, {'success': True})
        
    except Exception as e:
        return auth_module.response(start_response, {'error': str(e)})

def register(environ, start_response, auth_module): 
    try:
        auth_service = auth_module.env.get_service('auth_auth_service')
        body = auth_module.get_body(environ)
        if not body:
            return auth_module.response(start_response, {'error': 'Invalid request'})
        
        username = body.get('username')
        email = body.get('email')
        password = body.get('password')
        
        if not all([username, email, password]):
            return auth_module.response(start_response, {'error': 'All fields required'})
        
        if User.get(username=username):
            return auth_module.response(start_response, {'error': 'Username already exists'})
        
        if User.get(email=email):
            return auth_module.response(start_response, {'error': 'Email already exists'})
        
        password_hash = auth_service.hash_password(password)
        
        user_dict = User.create(
            username=username,
            email=email,
            password_hash=password_hash
        )
        
        return auth_module.response(start_response, {
            'success': True,
            'user': {
                'id': user_dict['id'],
                'username': user_dict['username'],
                'email': user_dict['email']
            }
        })
        
    except Exception as e:
        return auth_module.response(start_response, {'error': str(e)})

def profile(environ, start_response, auth_module): 
    try:
        user_dict = get_current_user(environ)
        if not user_dict:
            return auth_module.response(start_response, {'error': 'Not authenticated'})
        
        # Handle datetime serialization
        user_data = {
            'id': user_dict['id'],
            'username': user_dict['username'],
            'email': user_dict['email']
        }
        
        if user_dict.get('created_at'):
            if hasattr(user_dict['created_at'], 'isoformat'):
                user_data['created_at'] = user_dict['created_at'].isoformat()
            else:
                user_data['created_at'] = str(user_dict['created_at'])
                
        if user_dict.get('last_login'):
            if hasattr(user_dict['last_login'], 'isoformat'):
                user_data['last_login'] = user_dict['last_login'].isoformat()
            else:
                user_data['last_login'] = str(user_dict['last_login'])
        
        return auth_module.response(start_response, {'user': user_data})
        
    except Exception as e:
        return auth_module.response(start_response, {'error': str(e)})

def get_user(env, res, auth_module):
    route_params = env.get('ROUTE_PARAMS', {})
    user_id = route_params.get('id')
    if not user_id:
        return auth_module.response(res, {'error': 'User ID is required'})
    
    users = User.get(id=user_id)
    return auth_module.response(res, {'users': users})

def check_auth(environ, start_response, auth_module):
    try:
        auth_service = auth_module.env.get_service('auth_auth_service')
        user_dict = auth_service.get_current_user(environ)
        if user_dict:
            return auth_module.response(start_response, {
                'authenticated': True,
                'user': {
                    'id': user_dict['id'],
                    'username': user_dict['username']
                }
            })
        else:
            return auth_module.response(start_response, {
                'authenticated': False
            })
        
    except Exception as e:
        return auth_module.response(start_response, {'error': str(e)})
