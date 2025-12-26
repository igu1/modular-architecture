from modules.engine import BaseModule

class Invoices(BaseModule):
    dependencies = ['base', 'orders', 'accounts', 'contacts', 'products']
    
    def __init__(self):
        super().__init__()

    def initialize(self, env):
        super().initialize(env)
        self.subscribe_to_event('order_completed', self.on_order_completed)
        self.log("Invoices module initialized", "info")

    def on_order_completed(self, event_data):
        self.log(f"Order completed - generating invoice: {event_data}", "info")

    def load_routes(self):
        return super().load_routes()

    def deinitialize(self):
        pass
