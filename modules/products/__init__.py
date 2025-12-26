from modules.engine import BaseModule

class Products(BaseModule):
    dependencies = ['base']
    
    def __init__(self):
        super().__init__()

    def initialize(self, env):
        super().initialize(env)
        self.log("Products module initialized", "info")

    def load_routes(self):
        return super().load_routes()

    def deinitialize(self):
        pass
