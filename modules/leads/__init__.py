from modules.engine import BaseModule

class Leads(BaseModule):
    
    def __init__(self):
        super().__init__()
        self.dependencies = ['base', 'auth', 'crm']

    def initialize(self, env):
        super().initialize(env)
        self.setup_crm_integration()
        self.log("Leads module initialized", "info")

    def setup_crm_integration(self):
        crm_module = self.env.get_module('crm')
        if crm_module:
            self.log("CRM module detected - integration enabled", "info")
            self.subscribe_to_event('lead_created', self.on_lead_created)
        else:
            self.log("CRM module not found - running in standalone mode", "info")
    
    def on_lead_created(self, event_data):
        self.log(f"Lead created event received: {event_data.get('data')}", "info")

    def load_routes(self):
        return super().load_routes()

    def deinitialize(self):
        pass
