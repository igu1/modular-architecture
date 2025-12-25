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

        
    def load_module(self, module_name):
        if module_name in self.available_modules:
            module_path = f"modules.{module_name}"
            module = __import__(module_path, fromlist=[module_name])
            print("Initializing...")
            try:
                initializer = getattr(module, 'initialize', None)
                deinitializer = getattr(module, 'deinitialize', None)
                if not initializer:
                    raise NotImplementedError("Module does not support initialization")
                if not deinitializer:
                    raise NotImplementedError("Module does not support deinitialization")
                module = initializer(self.db_conn, self.shared_context)
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
    system.load_module("car")
    system.load_module("bike")
    system.list_modules()
    
    # Test bike creation functionality
    car_module = system.get_module("car")
    create_bike = getattr(car_module, 'create_bike')
    create_bike("Trek", "FX 2")
    
