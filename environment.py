class Environment:
    def __init__(self, registry):
        self._registry = registry
    
    def get_module(self, name):
        return self._registry.get_module(name)
    
    def get_available_module(self, name):
        return self._registry.get_available_module(name)
    
    def list_available_modules(self):
        return self._registry.list_available_modules()
    
    def list_loaded_modules(self):
        return self._registry.list_loaded_modules()
    
    def get_service(self, name):
        return self._registry.get_service(name)
    
    def list_services(self):
        return self._registry.list_services()
    
    def get_routes(self):
        return self._registry.get_routes()
    
    def get_module_for_route(self, route_path):
        """Get the module name that owns a specific route"""
        return self._registry.get_module_for_route(route_path)
    
    @property
    def registry(self):
        return self._registry
    
    def __getitem__(self, key):
        return self.get_module(key)
    
    def __getattr__(self, name):
        service = self.get_service(name)
        if service:
            return service
        module = self.get_module(name)
        if module:
            return module
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
    
    def get_status(self):
        return self._registry.get_status()
