from modules.engine import BaseModule

class CRM(BaseModule):
    dependencies = ['base']
    
    def __init__(self):
        super().__init__()

    def initialize(self, env):
        super().initialize(env)
        self.log("CRM base module initialized", "info")

    def get_models(self):
        from .models import Company
        return [Company]

    def load_routes(self):
        return super().load_routes()

    def deinitialize(self):
        pass
