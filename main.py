import sqlite3


class ModularSystem:
    def __init__(self):
        import modules
        self.available_modules = modules.modules
        self.modules = {}
        self.db_conn = next(self.initdb())
        self.shared_context = {}
        self.shared_context["events"] = {}
        self.shared_context['event_dispatcher'] = {
            "on": self.on,
            "emit": self.emit
        }
        self.routes = []

        
    def load_module(self, module_name):
        if module_name in self.available_modules:
            module_path = f"modules.{module_name}"
            module = __import__(module_path, fromlist=[module_name])
            print(f"Initializing module: {module_name}")
            try:
                # Get the class to check dependencies
                module_class = self.available_modules[module_name]
                temp_instance = module_class()
                module_deps = getattr(temp_instance, 'dependencies', [])
                print(f"Module dependencies: {module_deps}")
                
                # Load dependencies first
                #! TODO: The Module Init running twice in this way, its inefficient
                for dep in module_deps:
                    if dep not in self.modules and dep in self.available_modules:
                        print(f"Loading dependency: {dep}")
                        self.load_module(dep)
                    elif dep in self.modules:
                        print(f"Dependency already loaded: {dep}")
                    else:
                        raise ValueError(f"Module '{dep}' is not available but listed as dependency")

                initializer = getattr(module, 'initialize', None)
                deinitializer = getattr(module, 'deinitialize', None)
                if not initializer:
                    raise NotImplementedError("Module does not support initialization")
                if not deinitializer:
                    raise NotImplementedError("Module does not support deinitialization")
                module = initializer(self.db_conn, self.shared_context)
                load_routes_result = module.load_routes()
                try:
                    self.routes.extend(module.routes)
                    print(f"Added routes from module {module_name}")
                    print(f"Total routes loaded: {len(self.routes)}")
                    for route in module.routes:
                        print(f"  - {route}")
                except AttributeError:
                    print(f"Module {module_name} does not have a routes attribute, skipping route registration")
                    pass
                self.modules[module_name] = module
                self.shared_context['loaded_modules'] = self.modules
                print(f"Successfully loaded and initialized {module_name}")
            except Exception as e:
                print(f"Error initializing module {module_name}: {e}")
                import traceback
                traceback.print_exc()
                return False
            return True
        else:
            print(f"Module '{module_name}' not found")
            return False

    def on(self, event_name, callback):
        if event_name not in self.shared_context["events"]:
            self.shared_context["events"][event_name] = []
        self.shared_context["events"][event_name].append(callback)
    
    def emit(self, event_name: str, payload=None):
        events = self.shared_context["events"]
        handlers = events.get(event_name, [])

        for handler in handlers:
            try:
                handler(payload, self.shared_context)
            except Exception as e:
                print(f"Event handler error for {event_name}: {e}")

    def request_handler(self, environ, start_response):
        route = environ.get('PATH_INFO', '/')
        for route_item in self.routes:
            route_name, handler, method = route_item
            if route.startswith(route_name) and environ['REQUEST_METHOD'] == method:
                return handler(environ, start_response)
        
        status = '404 Not Found'
        headers = [('Content-type', 'text/plain')]
        start_response(status, headers)
        return [b"Page not found"]

    def initcontext(self):
        self.shared_context['loaded_modules'] = self.modules
        

    def initdb(self):
        print("Initializing database...")
        conn = sqlite3.connect('modular.db')
        yield conn

    def list_modules(self):
        for name, module in self.available_modules.items():
            status = "loaded" if name in self.modules else "not loaded"
            print(f"  {name}: {module.__name__} ({status})")

    def get_module(self, module_name):
        return self.modules.get(module_name)

if __name__ == "__main__":
    system = ModularSystem()
    system.initcontext()
    system.load_module("cart")
    system.list_modules()
    
    # Start the web server
    from wsgiref.simple_server import make_server

    print("API server would start on http://localhost:8080")
    print("Press Ctrl+C to stop")
    try:
        def wsgi_app(environ, start_response):
            return system.request_handler(environ, start_response)
        
        httpd = make_server('localhost', 8080, wsgi_app)
        print("Server running... Press Ctrl+C to stop")
        print("Server started successfully!")
        print("Visit http://localhost:8080 to see the server")
        print("Press Ctrl+C to stop the server")
        print("Use 'fuser -k 8080/tcp' to kill any existing processes")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")

