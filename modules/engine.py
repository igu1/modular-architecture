import json
import os
from urllib.parse import parse_qs

class BaseModule:
    def __init__(self):
        self.routes = []
    
    def get_info(self):
        module_path = self.__module__.replace(".", "/")
        manifest_path = f"{module_path}/manifest.json"
        with open(manifest_path, "r") as f:
            return json.load(f)

    def initialize(self, env):
        self.env = env
        
        db_session = self.env.get_service('db_session')
        if not db_session:
            raise RuntimeError("Database service not found in environment")
        
        models = self.get_models()
        if models:  
            for model in models:
                model.metadata.create_all(db_session().bind)
                print(f"Created tables for {model.__name__}")
    
    def get_db_session(self):
        db_session = self.env.get_service('db_session')
        return db_session() if db_session else None
    
    def get_other_module(self, name):
        return self.env.get_module(name)
        
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
        routes_path = f"{self.__module__}.routes"
        routes_module = __import__(routes_path, fromlist=["routes"])
        
        routes = []
        if hasattr(routes_module, 'url'):
            url_list = getattr(routes_module, 'url')
            if isinstance(url_list, list):
                routes.extend(url_list)
            elif isinstance(url_list, tuple):
                routes.append(url_list)
        
        return routes 

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