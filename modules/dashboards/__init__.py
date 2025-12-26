from modules.engine import BaseModule

class Dashboards(BaseModule):
    dependencies = ['base', 'auth']
    
    def __init__(self):
        super().__init__()

    def initialize(self, env):
        super().initialize(env)
        self.log("Dashboards module initialized", "info")

    def load_routes(self):
        return super().load_routes()

    def deinitialize(self):
        pass
