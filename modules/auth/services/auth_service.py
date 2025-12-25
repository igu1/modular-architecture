import hashlib
import secrets
from datetime import datetime, timedelta

class AuthService:
    def __init__(self):
        pass
    
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def generate_session_token(self):
        return secrets.token_urlsafe(32)

    def get_session_token(self, environ):
        auth_header = environ.get('HTTP_AUTHORIZATION', '')
        if auth_header.startswith('Bearer '):
            return auth_header[7:]
        return environ.get('HTTP_X_SESSION_TOKEN')

    def get_current_user(self, environ):
        # Import here to avoid circular dependencies
        from modules.auth.models import User, Session
        
        session_token = self.get_session_token(environ)
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

    def is_authenticated(self, environ):
        return self.get_current_user(environ) is not None

    def require_auth(self, environ, start_response, module):
        user = self.get_current_user(environ)
        if not user:
            return None
        return user

    def get_user_id(self, environ):
        user = self.get_current_user(environ)
        return user['id'] if user else None
