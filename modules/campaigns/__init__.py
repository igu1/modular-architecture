from modules.engine import BaseModule

class Campaigns(BaseModule):
    dependencies = ['base', 'contacts', 'leads']
    
    def __init__(self):
        super().__init__()

    def initialize(self, env):
        super().initialize(env)
        self.subscribe_to_event('lead_created', self.on_lead_created)
        self.log("Campaigns module initialized", "info")

    def on_lead_created(self, event_data):
        self.log(f"Lead created - tracking campaign source: {event_data}", "info")

    def load_routes(self):
        return super().load_routes()

    def deinitialize(self):
        pass
