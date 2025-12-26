from modules.engine import BaseModule

class Accounts(BaseModule):
    dependencies = ['base']
    
    def __init__(self):
        super().__init__()

    def initialize(self, env):
        super().initialize(env)
        self.subscribe_to_event('lead_converted', self.on_lead_converted)
        self.log("Accounts module initialized", "info")

    def on_lead_converted(self, event_data):
        self.log(f"Lead converted to account: {event_data}", "info")

    def load_routes(self):
        return super().load_routes()

    def deinitialize(self):
        pass
