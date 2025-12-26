from modules.engine import BaseModule

class Contacts(BaseModule):
    dependencies = ['base', 'accounts']
    
    def __init__(self):
        super().__init__()

    def initialize(self, env):
        super().initialize(env)
        self.subscribe_to_event('account_created', self.on_account_created)
        self.log("Contacts module initialized", "info")

    def on_account_created(self, event_data):
        self.log(f"Account created - auto-linking contacts: {event_data}", "info")

    def load_routes(self):
        return super().load_routes()

    def deinitialize(self):
        pass
