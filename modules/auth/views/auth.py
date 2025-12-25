import json
import hashlib
import secrets
from datetime import datetime, timedelta
from modules.auth.models import User, Session

def login(environ, start_response):
    auth_module = get_auth_module()
    try:
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
        
        password_hash = hash_password(password)
        if user_dict['password_hash'] != password_hash:
            return auth_module.response(start_response, {'error': 'Invalid credentials'})
        
        session_token = generate_session_token()
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

def logout(environ, start_response):
    auth_module = get_auth_module()
    try:
        session_token = get_session_token(environ)
        if session_token:
            session_dict = Session.get(session_token=session_token)
            if session_dict:
                Session.delete_record(session_dict['id'])
        
        return auth_module.response(start_response, {'success': True})
        
    except Exception as e:
        return auth_module.response(start_response, {'error': str(e)})

def register(environ, start_response):
    auth_module = get_auth_module()
    try:
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
        
        password_hash = hash_password(password)
        
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

def profile(environ, start_response):
    auth_module = get_auth_module()
    try:
        user_dict = get_current_user(environ)
        if not user_dict:
            return auth_module.response(start_response, {'error': 'Not authenticated'})
        
        return auth_module.response(start_response, {
            'user': {
                'id': user_dict['id'],
                'username': user_dict['username'],
                'email': user_dict['email'],
                'created_at': user_dict.get('created_at'),
                'last_login': user_dict.get('last_login')
            }
        })
        
    except Exception as e:
        return auth_module.response(start_response, {'error': str(e)})

def check_auth(environ, start_response):
    auth_module = get_auth_module()
    try:
        user_dict = get_current_user(environ)
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

def get_auth_module():
    import sys
    sys.path.append('/home/ez/tmp/modular')
    from modules.auth import Auth
    return Auth()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def generate_session_token():
    return secrets.token_urlsafe(32)

def get_session_token(environ):
    auth_header = environ.get('HTTP_AUTHORIZATION', '')
    if auth_header.startswith('Bearer '):
        return auth_header[7:]
    return environ.get('HTTP_X_SESSION_TOKEN')

def get_current_user(environ):
    session_token = get_session_token(environ)
    if not session_token:
        return None
    
    session_dict = Session.get(session_token=session_token)
    if not session_dict:
        return None
    
    # Check if session expired
    expires_at = session_dict.get('expires_at')
    if isinstance(expires_at, str):
        expires_at = datetime.fromisoformat(expires_at)
    
    if expires_at and expires_at < datetime.utcnow():
        Session.delete_record(session_dict['id'])
        return None
    
    return User.get(id=session_dict['user_id'])
