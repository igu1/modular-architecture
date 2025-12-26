from modules.engine import BaseModule

class EmailMarketing(BaseModule):
    dependencies = ['base', 'auth', 'campaigns', 'contacts']
    
    def __init__(self):
        super().__init__()

    def initialize(self, env):
        super().initialize(env)
        self.subscribe_to_event('campaign_created', self.on_campaign_created)
        self.log("Email Marketing module initialized", "info")

    def on_campaign_created(self, event_data):
        self.log(f"Campaign created - ready for email setup: {event_data}", "info")

    def load_routes(self):
        return super().load_routes()

    def deinitialize(self):
        pass
