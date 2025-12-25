import re
from database import init_db, get_session
from registry import Registry
from environment import Environment

class ModularSystem:
    def __init__(self):
        init_db("sqlite:///test.db")
        self.registry = Registry()
        self.env = Environment(self.registry)
        self.registry.register_service('db_session', get_session)
        import modules
        self.registry.set_available_modules(modules.modules)


    def load_module(self, module_name):
        module_class = self.env.get_available_module(module_name)
        if not module_class:
            print(f"Module '{module_name}' not found in available modules")
            return False
        
        print(f"Initializing module: {module_name}")
        try:
            temp_instance = module_class()
            module_deps = getattr(temp_instance, 'dependencies', [])
            
            for dep in module_deps:
                if dep not in self.env.list_loaded_modules() and dep in self.env.list_available_modules():
                    self.load_module(dep)
                elif dep in self.env.list_loaded_modules():
                    pass
                else:
                    raise ValueError(f"Module '{dep}' is not available but listed as dependency")

            try:
                routes = module_class().load_routes()
                self.registry.add_routes(routes, module_name)
            except AttributeError:
                pass

            module_instance = module_class()
            module_instance.initialize(self.env)
            self.registry.register_module(module_name, module_instance)
            
            return True
            
        except Exception as e:
            print(f"Error initializing module {module_name}: {e}")
            import traceback
            traceback.print_exc()
            return False

    def list_modules(self):
        available_modules = self.env.list_available_modules()
        loaded_modules = self.env.list_loaded_modules()
        
        for name in available_modules:
            module_class = self.env.get_available_module(name)
            status = "loaded" if name in loaded_modules else "not loaded"
            print(f"  {name}: {module_class.__class__.__name__} ({status})")

    def get_module(self, module_name):
        return self.env.get_module(module_name)

    def load_manifest(self):
        loaded_modules = self.env.list_loaded_modules()
        for name in loaded_modules:
            module = self.env.get_module(name)
            manifest = module.get_info()

    def _match_route(self, route, route_name):
        import re
        pattern = route_name
        pattern = re.sub(r'<(\w+)>', r'(?P<\1>[^/]+)', pattern)
        pattern = f'^{pattern}$'
        match = re.match(pattern, route)
        if match:
            return True, match.groupdict()
        return False, {}
    
    def _create_handler_with_module(self, handler, module_instance, route_params=None):
        def wrapped_handler(environ, start_response):
            environ['ROUTE_PARAMS'] = route_params or {}
            return handler(environ, start_response, module_instance)
        return wrapped_handler
    
    def request_handler(self, environ, start_response):
        route = environ.get('PATH_INFO', '/')
        method = environ['REQUEST_METHOD']
        
        for route_name, route_method, handler in self.env.get_routes():
            matches, params = self._match_route(route, route_name)
            if matches and method == route_method:
                module_name = self.env.get_module_for_route(route_name)
                if module_name:
                    module_instance = self.env.get_module(module_name)
                    return self._create_handler_with_module(handler, module_instance, params)(environ, start_response)
                return self._create_handler_with_module(handler, None, params)(environ, start_response)
        
        return self._404_response(start_response)
    
    def _404_response(self, start_response):
        start_response('404 Not Found', [('Content-type', 'text/plain')])
        return [b"Page not found"]

if __name__ == "__main__":
    system = ModularSystem()
    system.load_module('base')
    system.load_module('auth')
    system.load_manifest()
    system.list_modules()
    
    print(f"\n=== Registry Status ===")
    status = system.env.get_status()
    for key, value in status.items():
        print(f"{key}: {value}")

    from wsgiref.simple_server import make_server

    try:
        def wsgi_app(environ, start_response):
            return system.request_handler(environ, start_response)
        
        httpd = make_server('localhost', 8080, wsgi_app)
        print("\nServer running... Press Ctrl+C to stop")
        print("Visit http://localhost:8080 to see the server")
        print("Press Ctrl+C to stop the server")
        print("Use 'fuser -k 8080/tcp' to kill any existing processes")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")

