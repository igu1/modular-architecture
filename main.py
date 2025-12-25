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
            print(f"Initializing module: {module_name}")
            try:
                module_deps = getattr(module, 'dependencies', [])
                print(f"Module dependencies: {module_deps}")
                
                # Load dependencies first
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
    system.load_module("product")
    system.load_module("cart")
    system.load_module("checkout")
    system.list_modules()
    
    # Test e-commerce functionality
    # print("Testing e-commerce functionality...")
    # product_module = system.get_module("product")
    # add_product = getattr(product_module, 'add_product')
    # add_product("Laptop", 999.99, "Electronics")
    # add_product("Book", 19.99, "Education")
    
    # # Test cart functionality
    # cart_module = system.get_module("cart")
    # add_to_cart = getattr(cart_module, 'add_to_cart')
    # add_to_cart(1, 2)  # Add 2 laptops to cart
    # add_to_cart(2, 1)  # Add 1 book to cart
    
    # # View cart before checkout
    # view_cart = getattr(cart_module, 'view_cart')
    # print(f"Cart contents before checkout: {view_cart()}")
    
    checkout_module = system.get_module("checkout")
    checkout = getattr(checkout_module, 'checkout')
    result = checkout("credit_card")
    print(f"Checkout result: {result}")
    
