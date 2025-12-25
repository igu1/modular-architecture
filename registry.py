class Registry:
    def __init__(self):
        self.modules = {}
        self.services = {}
        self.routes = []
        self.route_to_module = {}
        self.available_modules = {}
        
    
    def register_module(self, name, module):
        self.modules[name] = module
    
    def get_module(self, name):
        return self.modules.get(name)
    
    def set_available_modules(self, modules_dict):
        self.available_modules = modules_dict
    
    def get_available_module(self, name):
        return self.available_modules.get(name)
    
    def list_available_modules(self):
        return list(self.available_modules.keys())
    
    def list_loaded_modules(self):
        return list(self.modules.keys())
    
    def register_service(self, name, service):
        self.services[name] = service
    
    def get_service(self, name):
        return self.services.get(name)
    
    def list_services(self):
        return list(self.services.keys())
    
    def add_routes(self, routes, module_name=None):
        if isinstance(routes, list):
            self.routes.extend(routes)
            if module_name:
                for route in routes:
                    if isinstance(route, tuple) and len(route) >= 3:
                        route_path = route[0]
                        self.route_to_module[route_path] = module_name
        else:
            self.routes.append(routes)
            if module_name and isinstance(routes, tuple) and len(routes) >= 3:
                route_path = routes[0]
                self.route_to_module[route_path] = module_name
    
    def get_routes(self):
        return self.routes
    
    def clear_routes(self):
        self.routes = []
    
    def get_module_for_route(self, route_path):
        """Get the module name that owns a specific route"""
        return self.route_to_module.get(route_path)
    
    def get_status(self):
        return {
            'loaded_modules': len(self.modules),
            'available_modules': len(self.available_modules),
            'services': len(self.services),
            'routes': len(self.routes)
        }
