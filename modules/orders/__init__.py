from modules.engine import BaseModule

class Orders(BaseModule):
    dependencies = ['base', 'auth', 'quotes', 'opportunities', 'accounts', 'contacts', 'products']
    
    def __init__(self):
        super().__init__()

    def initialize(self, env):
        super().initialize(env)
        self.subscribe_to_event('quote_accepted', self.on_quote_accepted)
        self.log("Orders module initialized", "info")

    def on_quote_accepted(self, event_data):
        self.log(f"Quote accepted - creating order: {event_data}", "info")

    def load_routes(self):
        return super().load_routes()

    def deinitialize(self):
        pass
