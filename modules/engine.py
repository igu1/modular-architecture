import json
import os
from urllib.parse import parse_qs

class BaseModule:
    def __init__(self):
        self.routes = self.load_routes()
    
    def get_info(self):
        module_path = self.__module__.replace(".", "/")
        manifest_path = f"{module_path}/manifest.json"
        with open(manifest_path, "r") as f:
            return json.load(f)

    def initialize(self, db_conn, shared_context):
        self.db_conn = db_conn
        self.shared_context = shared_context

        models = self.get_models()
        if models:  
            for model in models:
                model.metadata.create_all(self.db_conn)
                print(f"Created tables for {model.__name__}")

    def get_models(self):
        models_path = f"{self.__module__}.models"
        models_module = __import__(models_path, fromlist=["models"])
        
        model_classes = []
        for attr_name in dir(models_module):
            attr = getattr(models_module, attr_name)
            if isinstance(attr, type) and hasattr(attr, '__tablename__'):
                model_classes.append(attr)
        
        return model_classes

    def deinitialize(self):
        pass

    def load_routes(self):
        return []
    
    def get_routes(self):
        return self.routes

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
    
    def get_manifest(self):
        return self.get_info()