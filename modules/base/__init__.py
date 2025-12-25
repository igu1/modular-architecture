from modules.engine import BaseModule

class Base(BaseModule):
    
    def __init__(self):
        super().__init__()

    def initialize(self, env):
        super().initialize(env)
        self.setup_event_handlers()

    def setup_event_handlers(self):
        pass

    def load_routes(self):
        return super().load_routes()

    def deinitialize(self):
        pass