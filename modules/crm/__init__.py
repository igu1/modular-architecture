from modules.engine import BaseModule

class CRM(BaseModule):
    
    def __init__(self):
        super().__init__()
        self.dependencies = ['base', 'auth']

    def initialize(self, env):
        super().initialize(env)
        self.log("CRM base module initialized", "info")

    def load_routes(self):
        return super().load_routes()

    def deinitialize(self):
        pass
