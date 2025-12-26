from modules.engine import BaseModule

class Newsletter(BaseModule):
    
    def __init__(self):
        super().__init__()
        self.dependencies = ['base', 'auth', 'crm']

    def initialize(self, env):
        super().initialize(env)
        self.setup_integrations()
        self.log("Newsletter module initialized", "info")

    def setup_integrations(self):
        crm_module = self.env.get_module('crm')
        if crm_module:
            self.log("CRM module detected - integration enabled", "info")
        
        customers_module = self.env.get_module('customers')
        if customers_module:
            self.log("Customers module detected - subscribing to customer events", "info")
            self.subscribe_to_event('customer_created', self.on_customer_created)
        else:
            self.log("Customers module not found - running without customer integration", "info")
    
    def on_customer_created(self, event_data):
        data = event_data.get('data', {})
        self.log(f"New customer for potential newsletter subscription: {data.get('email')}", "info")

    def load_routes(self):
        return super().load_routes()

    def deinitialize(self):
        pass
