from modules.engine import BaseModule

class Customers(BaseModule):
    
    def __init__(self):
        super().__init__()
        self.dependencies = ['base', 'crm', 'leads']

    def initialize(self, env):
        super().initialize(env)
        self.setup_integrations()
        self.log("Customers module initialized", "info")

    def setup_integrations(self):
        crm_module = self.env.get_module('crm')
        if crm_module:
            self.log("CRM module detected - integration enabled", "info")
        
        leads_module = self.env.get_module('leads')
        if leads_module:
            self.log("Leads module detected - subscribing to lead conversion events", "info")
            self.subscribe_to_event('lead_converted', self.on_lead_converted)
        else:
            self.log("Leads module not found - running without lead conversion", "info")
    
    def on_lead_converted(self, event_data):
        data = event_data.get('data', {})
        self.log(f"Lead converted to customer: {data.get('name')}", "info")

    def load_routes(self):
        return super().load_routes()

    def deinitialize(self):
        pass
