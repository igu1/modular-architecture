class Registry:
    def __init__(self):
        self.modules = {}
        self.services = {}
        self.available_modules = {}
        self.routes = []
        
    
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
    
    def add_routes(self, routes):
        if isinstance(routes, list):
            self.routes.extend(routes)
        else:
            self.routes.append(routes)
    
    def get_routes(self):
        return self.routes
    
    def clear_routes(self):
        self.routes = []
    
    def get_status(self):
        return {
            'loaded_modules': len(self.modules),
            'available_modules': len(self.available_modules),
            'services': len(self.services),
            'routes': len(self.routes)
        }
