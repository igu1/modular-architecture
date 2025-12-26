from modules.engine import BaseModule

class Quotes(BaseModule):
    dependencies = ['base', 'auth', 'opportunities', 'accounts', 'contacts', 'products']
    
    def __init__(self):
        super().__init__()

    def initialize(self, env):
        super().initialize(env)
        self.subscribe_to_event('opportunity_updated', self.on_opportunity_updated)
        self.log("Quotes module initialized", "info")

    def on_opportunity_updated(self, event_data):
        self.log(f"Opportunity updated - may need quote update: {event_data}", "info")

    def load_routes(self):
        return super().load_routes()

    def deinitialize(self):
        pass
