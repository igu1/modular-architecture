class Registry:
    def __init__(self):
        self.modules = {}
        self.services = {}
        self.routes = []
        self.route_to_module = {}
        self.available_modules = {}
        
        self._subscribers = {} 
        self._extension_hooks = {}
        
        from logger import core_logger
        self.logger = core_logger
        
    
    def register_module(self, name, module):
        self.modules[name] = module
    
    def get_module(self, name):
        return self.modules.get(name)
    
    def set_available_modules(self, modules_dict):
        self.available_modules = modules_dict
    
    def get_available_module(self, name):
        return self.available_modules.get(name)
    
    def load_module(self, module_name, env):
        module_class = self.get_available_module(module_name)
        if not module_class:
            self.logger.log("registry", f"Module '{module_name}' not found in available modules", "warning")
            return False
        
        self.logger.log("registry", f"Initializing module: {module_name}", "info")
        try:
            temp_instance = module_class()
            module_deps = getattr(temp_instance, 'dependencies', [])
            
            for dep in module_deps:
                if dep not in self.list_loaded_modules() and dep in self.list_available_modules():
                    self.load_module(dep, env)
                elif dep in self.list_loaded_modules():
                    pass
                else:
                    error_msg = f"Module '{dep}' is not available but listed as dependency"
                    self.logger.log("registry", error_msg, "error")
                    raise ValueError(error_msg)

            try:
                routes = module_class().load_routes()
                self.add_routes(routes, module_name)
            except AttributeError:
                pass

            module_instance = module_class()
            module_instance.initialize(env)
            self.register_module(module_name, module_instance)
            
            self._trigger_hook('module_loaded', module_name, module_instance, env)
            
            return True
            
        except Exception as e:
            self.logger.log("registry", f"Error initializing module {module_name}: {e}", "error")
            import traceback
            self.logger.log("registry", f"Traceback: {traceback.format_exc()}", "error")
            return False
    
    def list_available_modules(self):
        return list(self.available_modules.keys())
    
    def list_loaded_modules(self):
        return list(self.modules.keys())
    
    def register_service(self, name, service):
        self.services[name] = service
        self.logger.log("registry", f"Registered service: {name}", "debug")
    
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
    
    # PubSub System Methods
    def subscribe(self, event_name, module_name, callback_func):
        """Subscribe to an event with a callback function"""
        if event_name not in self._subscribers:
            self._subscribers[event_name] = set()
        
        self._subscribers[event_name].add((module_name, callback_func))
        self.logger.log("registry", f"Module '{module_name}' subscribed to event '{event_name}'", "info")
    
    def unsubscribe(self, event_name, module_name, callback_func=None):
        """Unsubscribe from an event"""
        if event_name not in self._subscribers:
            return
        
        if callback_func:
            self._subscribers[event_name].discard((module_name, callback_func))
        else:
            # Remove all subscriptions for this module
            self._subscribers[event_name] = {
                (mod, callback) for mod, callback in self._subscribers[event_name]
                if mod != module_name
            }
        
        self.logger.log("registry", f"Module '{module_name}' unsubscribed from event '{event_name}'", "info")
    
    def emit(self, event_name, data=None, source_module=None):
        """Emit an event to all subscribers"""
        if event_name not in self._subscribers:
            return
        
        event_data = {
            'event_name': event_name,
            'data': data,
            'source': source_module,
            'timestamp': __import__('datetime').datetime.utcnow().isoformat()
        }
        
        self.logger.log("registry", f"Emitting event '{event_name}' from module '{source_module}' to {len(self._subscribers[event_name])} subscribers", "info")
        self.logger.log_event(event_data)
        
        for module_name, callback_func in self._subscribers[event_name]:
            try:
                module = self.get_module(module_name)
                if module:
                    callback_func(event_data)
                else:
                    self.logger.log("registry", f"Warning: Module '{module_name}' not found for event '{event_name}'", "warning")
            except Exception as e:
                self.logger.log("registry", f"Error in event handler for '{event_name}' in module '{module_name}': {e}", "error")
    
    def list_subscriptions(self):
        """List all event subscriptions"""
        subscriptions = {}
        for event_name, subscribers in self._subscribers.items():
            subscriptions[event_name] = [module_name for module_name, _ in subscribers]
        return subscriptions
    
    def register_hook(self, hook_name, callback):
        """Register a hook callback for runtime extensions"""
        if hook_name not in self._extension_hooks:
            self._extension_hooks[hook_name] = []
        self._extension_hooks[hook_name].append(callback)
    
    def _trigger_hook(self, hook_name, *args, **kwargs):
        """Trigger all callbacks registered for a hook"""
        if hook_name in self._extension_hooks:
            for callback in self._extension_hooks[hook_name]:
                try:
                    callback(*args, **kwargs)
                except Exception as e:
                    self.logger.log("registry", f"Error in hook '{hook_name}': {e}", "error")
