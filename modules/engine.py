import json
import os
import importlib
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
        
        # Load module services
        self.load_services()
        
        db_service = self.env.get_service('db_service')
        if not db_service:
            raise RuntimeError("Database service not found in environment")
        
        models = self.get_models()
        if models:  
            db_session = db_service.get_session()
            for model in models:
                model.metadata.create_all(db_session().bind)
                self.log(f"Created tables for {model.__name__}", "info")
    
    def load_services(self):
        """Automatically load services from the module's services directory"""
        services_path = f"{self.__module__.replace('.', '/')}/services"
        if not os.path.exists(services_path):
            return
        
        service_files = [f for f in os.listdir(services_path) 
                        if f.endswith('.py') and not f.startswith('__')]
        
        for service_file in service_files:
            service_name = service_file[:-3]  # Remove .py extension
            try:
                # Import the service module
                service_module_path = f"{self.__module__}.services.{service_name}"
                service_module = importlib.import_module(service_module_path)
                
                # Look for service classes (typically ending with 'Service')
                for attr_name in dir(service_module):
                    attr = getattr(service_module, attr_name)
                    if (isinstance(attr, type) and 
                        attr_name.endswith('Service') and 
                        hasattr(attr, '__init__')):
                        
                        # Instantiate and register the service
                        service_instance = attr()
                        module_name = self.__module__.split('.')[-1]
                        
                        # Base module services don't need prefix (foundational services)
                        if module_name == 'base':
                            service_key = service_name
                        else:
                            service_key = f"{module_name}_{service_name}"
                            
                        self.env.register_service(service_key, service_instance)
                        self.log(f"Loaded service: {service_key}", "info")
                        break
                        
            except Exception as e:
                self.log(f"Error loading service {service_name}: {e}", "error")
    
    def get_db_session(self):
        db_service = self.env.get_service('db_service')
        return db_service.get_session() if db_service else None
    
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
        if hasattr(routes_module, 'routes'):
            route_list = getattr(routes_module, 'routes')
            if isinstance(route_list, list):
                routes.extend(route_list)
            elif isinstance(route_list, tuple):
                routes.append(route_list)
        elif hasattr(routes_module, 'url'):
            url_list = getattr(routes_module, 'url')
            if isinstance(url_list, list):
                routes.extend(url_list)
            elif isinstance(url_list, tuple):
                routes.append(url_list)

        return routes 

    def response(self, start_response, data, status='200 OK'):
        response_data = json.dumps(data).encode('utf-8')
        start_response(status, [('Content-Type', 'application/json'), ('Content-Length', str(len(response_data)))])
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
                self.log(f"JSON decode error: {e}", "error")
                self.log(f"Body text: '{body_text}'", "error")
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
    
    # PubSub System Methods for Modules
    def subscribe_to_event(self, event_name, callback_func):
        """Subscribe to an event with a callback function"""
        module_name = self.__module__.split('.')[-1]
        self.env.registry.subscribe(event_name, module_name, callback_func)
    
    def unsubscribe_from_event(self, event_name, callback_func=None):
        """Unsubscribe from an event"""
        module_name = self.__module__.split('.')[-1]
        self.env.registry.unsubscribe(event_name, module_name, callback_func)
    
    def emit_event(self, event_name, data=None):
        """Emit an event to all subscribers"""
        module_name = self.__module__.split('.')[-1]
        self.env.registry.emit(event_name, data, module_name)
    
    def on_event(self, event_name):
        """Decorator to easily subscribe to events"""
        def decorator(callback_func):
            self.subscribe_to_event(event_name, callback_func)
            return callback_func
        return decorator
    
    def log(self, message, level='info'):
        module_name = self.__module__.split('.')[-1]
        if hasattr(self, 'env') and hasattr(self.env, 'logger'):
            self.env.logger.log(module_name, message, level)
        else:
            # Use base logger as fallback
            from logger import core_logger
            core_logger.log(module_name, message, level)