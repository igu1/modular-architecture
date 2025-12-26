import re
from registry import Registry
from environment import Environment
from logger import CoreLogger

class ModularSystem:
    def __init__(self):
        self.registry = Registry()
        self.env = Environment(self.registry)
        self.logger = CoreLogger()
        import modules
        self.registry.set_available_modules(modules.modules)


    def load_module(self, module_name):
        module_class = self.env.get_available_module(module_name)
        if not module_class:
            return False
        
        return self.registry.load_module(module_name, self.env)

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
            
            # If handler is a string path, import it
            if isinstance(handler, str):
                module_path, func_name = handler.rsplit('.', 1)
                handler_module = __import__(module_path, fromlist=[func_name])
                handler_func = getattr(handler_module, func_name)
                return handler_func(environ, start_response, module_instance)
            else:
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
    system.load_module('leads')
    system.load_manifest()

    from wsgiref.simple_server import make_server

    try:
        def wsgi_app(environ, start_response):
            return system.request_handler(environ, start_response)
        
        httpd = make_server('localhost', 8080, wsgi_app)
        system.logger.log("core", "\nServer running... Press Ctrl+C to stop", "info")
        system.logger.log("core", "Visit http://localhost:8080 to see the server", "info")
        system.logger.log("core", "Press Ctrl+C to stop the server", "info")
        system.logger.log("core", "Use 'fuser -k 8080/tcp' to kill any existing processes", "info")
        httpd.serve_forever()
    except KeyboardInterrupt:
        system.logger.log("core", "\nServer stopped.", "info")

