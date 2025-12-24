import sqlite3

class ModularSystem:
    def __init__(self):
        import modules
        self.available_modules = modules.modules
        self.modules = {}
        self.db_conn = next(self.initdb())
        self.shared_context = {}

        
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
                # Update shared context after each module loads
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
    
    # Test bike count functionality
    print("Testing bike count functionality...")
    car_module = system.get_module("car")
    getbikes = getattr(car_module, 'get_bikes')
    print(f"Get bikes: {getbikes()}")
    
    # Test direct access to bike module
    bike_module = system.get_module("bike")
    print(f"Direct bike access: {bike_module.get_bikes()}")