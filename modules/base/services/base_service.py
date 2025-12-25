import logging
from datetime import datetime

class BaseService:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info(f"Initialized {self.__class__.__name__}")
    
    def log_activity(self, message, level='info'):
        """Log activity with timestamp"""
        timestamp = datetime.utcnow().isoformat()
        log_message = f"[{timestamp}] {message}"
        
        if level == 'info':
            self.logger.info(log_message)
        elif level == 'error':
            self.logger.error(log_message)
        elif level == 'warning':
            self.logger.warning(log_message)
        elif level == 'debug':
            self.logger.debug(log_message)
    
    def get_timestamp(self):
        """Get current UTC timestamp"""
        return datetime.utcnow()
    
    def format_response(self, success=True, data=None, error=None):
        """Standard response format"""
        response = {'success': success}
        if data is not None:
            response['data'] = data
        if error is not None:
            response['error'] = error
        return response
