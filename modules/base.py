import json
from urllib.parse import parse_qs

class BaseModule:
    def __init__(self):
        pass
    
    def get_info(self):
        return {"name": self.__class__.__name__, "module": self.__class__.__module__, "type": "base"}

    def initialize(self):
        raise NotImplementedError("Subclasses must implement initialize method")
    
    def deinitialize(self):
        raise NotImplementedError("Subclasses must implement deinitialize method")

    def load_routes(self):
        raise NotImplementedError("Subclasses must implement load_routes method")
    
    def get_routes(self):
        return []

    def response(self, start_response, data):
        response_data = json.dumps(data).encode('utf-8')
        start_response('200 OK', [('Content-Type', 'application/json'), ('Content-Length', str(len(response_data)))])
        return [response_data]
    
    def get_body(self, environ):
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
                print(f"JSON decode error: {e}")
                print(f"Body text: '{body_text}'")
                return None
        return {}
    
    def get_params(self, environ):
        query_string = environ.get("QUERY_STRING", "")
        params = parse_qs(query_string)
        for key, value in params.items():
            params[key] = value[0]
        return params