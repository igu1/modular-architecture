from datetime import datetime

class CRMService:
    def __init__(self):
        pass
    
    def get_timestamp(self):
        return datetime.utcnow().isoformat()
    
    def format_response(self, success=True, data=None, error=None):
        response = {'success': success}
        if data is not None:
            response['data'] = data
        if error is not None:
            response['error'] = error
        return response
