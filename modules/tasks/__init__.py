from modules.engine import BaseModule

class Tasks(BaseModule):
    dependencies = ['base', 'auth', 'accounts', 'contacts', 'opportunities']
    
    def __init__(self):
        super().__init__()

    def initialize(self, env):
        super().initialize(env)
        self.subscribe_to_event('opportunity_created', self.on_opportunity_created)
        self.log("Tasks module initialized", "info")

    def on_opportunity_created(self, event_data):
        self.log(f"Opportunity created - creating follow-up tasks: {event_data}", "info")

    def load_routes(self):
        return super().load_routes()

    def deinitialize(self):
        pass
