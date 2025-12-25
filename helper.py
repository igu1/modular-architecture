import json
import os
from urllib.parse import parse_qs, urlparse
from datetime import datetime
import hashlib
import secrets
from typing import Dict, Any, Optional, Union, List, Tuple
from logger import core_logger


class WSGIHelpers:
    """WSGI utility functions for handling requests and responses"""
    
    @staticmethod
    def response(start_response, data: Union[str, Dict, Any], status: str = "200 OK", content_type: str = "application/json"):
        """Create a WSGI response"""
        if isinstance(data, (dict, list)):
            response_data = json.dumps(data).encode('utf-8')
        else:
            response_data = str(data).encode('utf-8')
            if content_type == "application/json":
                content_type = "text/plain"
        
        headers = [
            ('Content-Type', content_type),
            ('Content-Length', str(len(response_data))),
            ('Access-Control-Allow-Origin', '*'),
            ('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS'),
            ('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        ]
        
        start_response(status, headers)
        return [response_data]
    
    @staticmethod
    def json_response(start_response, data: Dict[str, Any], status: str = "200 OK"):
        """Create a JSON response"""
        return WSGIHelpers.response(start_response, data, status, "application/json")
    
    @staticmethod
    def html_response(start_response, html: str, status: str = "200 OK"):
        """Create an HTML response"""
        return WSGIHelpers.response(start_response, html, status, "text/html")
    
    @staticmethod
    def error_response(start_response, message: str, status: str = "400 Bad Request"):
        """Create an error response"""
        return WSGIHelpers.json_response(start_response, {"error": message}, status)
    
    @staticmethod
    def get_body(environ) -> Optional[Dict[str, Any]]:
        """Extract and parse JSON body from WSGI environ"""
        try:
            content_length = int(environ.get("CONTENT_LENGTH", 0))
        except (ValueError, TypeError):
            content_length = 0
        
        if content_length > 0:
            body_bytes = environ["wsgi.input"].read(content_length)
            body_text = body_bytes.decode("utf-8")
            if not body_text.strip():
                return {}
            try:
                body = json.loads(body_text)
                return body
            except json.JSONDecodeError as e:
                core_logger.log("helper", f"JSON decode error: {e}", "error")
                core_logger.log("helper", f"Body text: '{body_text}'", "error")
                return None
        return {}
    
    @staticmethod
    def get_params(environ) -> Dict[str, str]:
        """Extract query parameters from WSGI environ"""
        query_string = environ.get("QUERY_STRING", "")
        params = parse_qs(query_string)
        # Convert single-value lists to strings
        result = {}
        for key, value in params.items():
            result[key] = value[0] if len(value) == 1 else value
        return result
    
    @staticmethod
    def get_path_info(environ) -> str:
        """Get the path info from WSGI environ"""
        return environ.get('PATH_INFO', '/')
    
    @staticmethod
    def get_method(environ) -> str:
        """Get the HTTP method from WSGI environ"""
        return environ.get('REQUEST_METHOD', 'GET')
    
    @staticmethod
    def get_headers(environ) -> Dict[str, str]:
        """Extract HTTP headers from WSGI environ"""
        headers = {}
        for key, value in environ.items():
            if key.startswith('HTTP_'):
                header_name = key[5:].replace('_', '-').title()
                headers[header_name] = value
        return headers


class AuthHelpers:
    """Authentication and authorization utilities"""
    
    @staticmethod
    def generate_token(length: int = 32) -> str:
        """Generate a secure random token"""
        return secrets.token_urlsafe(length)
    
    @staticmethod
    def hash_password(password: str, salt: Optional[str] = None) -> Tuple[str, str]:
        """Hash a password with salt"""
        if salt is None:
            salt = secrets.token_hex(16)
        
        password_hash = hashlib.pbkdf2_hmac('sha256', 
                                         password.encode('utf-8'), 
                                         salt.encode('utf-8'), 
                                         100000)
        return password_hash.hex(), salt
    
    @staticmethod
    def verify_password(password: str, password_hash: str, salt: str) -> bool:
        """Verify a password against its hash"""
        hash_calc, _ = AuthHelpers.hash_password(password, salt)
        return secrets.compare_digest(hash_calc, password_hash)
    
    @staticmethod
    def get_bearer_token(environ) -> Optional[str]:
        """Extract Bearer token from Authorization header"""
        headers = WSGIHelpers.get_headers(environ)
        auth_header = headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            return auth_header[7:]
        return None


class DatabaseHelpers:
    """Database utility functions"""
    
    @staticmethod
    def model_to_dict(model_instance) -> Dict[str, Any]:
        """Convert SQLAlchemy model instance to dictionary"""
        if hasattr(model_instance, '__table__'):
            return {c.name: getattr(model_instance, c.name) 
                   for c in model_instance.__table__.columns}
        return {}
    
    @staticmethod
    def models_to_list(model_instances) -> List[Dict[str, Any]]:
        """Convert list of SQLAlchemy model instances to list of dictionaries"""
        return [DatabaseHelpers.model_to_dict(instance) for instance in model_instances]
    
    @staticmethod
    def paginate_query(query, page: int = 1, per_page: int = 10):
        """Paginate a SQLAlchemy query"""
        total = query.count()
        items = query.offset((page - 1) * per_page).limit(per_page).all()
        
        return {
            'items': DatabaseHelpers.models_to_list(items),
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': (total + per_page - 1) // per_page
        }


class ValidationHelpers:
    """Data validation utilities"""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Simple email validation"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> Tuple[bool, List[str]]:
        """Validate that required fields are present and not empty"""
        missing = []
        for field in required_fields:
            if field not in data or data[field] is None or str(data[field]).strip() == '':
                missing.append(field)
        
        return len(missing) == 0, missing
    
    @staticmethod
    def sanitize_string(text: str, max_length: int = None) -> str:
        """Sanitize string input"""
        if not isinstance(text, str):
            text = str(text)
        
        # Remove potentially dangerous characters
        dangerous_chars = ['<', '>', '"', "'", '&', '\x00']
        for char in dangerous_chars:
            text = text.replace(char, '')
        
        if max_length and len(text) > max_length:
            text = text[:max_length]
        
        return text.strip()


class FileHelpers:
    """File and directory utilities"""
    
    @staticmethod
    def ensure_directory(path: str) -> bool:
        """Ensure a directory exists"""
        try:
            os.makedirs(path, exist_ok=True)
            return True
        except OSError:
            return False
    
    @staticmethod
    def get_file_size(file_path: str) -> int:
        """Get file size in bytes"""
        try:
            return os.path.getsize(file_path)
        except OSError:
            return 0
    
    @staticmethod
    def file_exists(file_path: str) -> bool:
        """Check if file exists"""
        return os.path.isfile(file_path)
    
    @staticmethod
    def get_file_extension(filename: str) -> str:
        """Get file extension from filename"""
        return os.path.splitext(filename)[1].lower()
    
    @staticmethod
    def is_safe_filename(filename: str) -> bool:
        """Check if filename is safe (no path traversal)"""
        dangerous_patterns = ['..', '/', '\\', ':', '*', '?', '"', '<', '>', '|']
        return not any(pattern in filename for pattern in dangerous_patterns)


class CacheHelpers:
    """Simple caching utilities"""
    
    def __init__(self):
        self._cache = {}
    
    def get(self, key: str, default=None):
        """Get value from cache"""
        item = self._cache.get(key)
        if item:
            value, expiry = item
            if expiry is None or expiry > datetime.now():
                return value
            else:
                # Expired, remove from cache
                del self._cache[key]
        return default
    
    def set(self, key: str, value, ttl_seconds: int = None):
        """Set value in cache with optional TTL"""
        expiry = None
        if ttl_seconds:
            from datetime import timedelta
            expiry = datetime.now() + timedelta(seconds=ttl_seconds)
        
        self._cache[key] = (value, expiry)
    
    def delete(self, key: str):
        """Delete key from cache"""
        self._cache.pop(key, None)
    
    def clear(self):
        """Clear all cache"""
        self._cache.clear()


class LoggingHelpers:
    """Logging utilities"""
    
    @staticmethod
    def log_request(environ, response_status: str = None):
        """Log HTTP request details"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        method = WSGIHelpers.get_method(environ)
        path = WSGIHelpers.get_path_info(environ)
        user_agent = environ.get('HTTP_USER_AGENT', 'Unknown')
        ip = environ.get('REMOTE_ADDR', 'Unknown')
        
        log_entry = f"{ip} - {method} {path} - {user_agent}"
        if response_status:
            log_entry += f" - {response_status}"
        
        core_logger.log("http", log_entry, "info")
    
    @staticmethod
    def log_error(message: str, exception: Exception = None):
        """Log error with optional exception details"""
        error_msg = message
        
        if exception:
            error_msg += f" - {type(exception).__name__}: {str(exception)}"
        
        core_logger.log("helper", error_msg, "error")


# Global instances for easy access
cache = CacheHelpers()