from modules.engine import BaseModule

class Base(BaseModule):
    
    def __init__(self):
        super().__init__()

    def initialize(self, env):
        super().initialize(env)
        
        # session = self.get_db_session()
        # other_module = self.get_other_module('auth')

    def load_routes(self):
        return super().load_routes()

    def deinitialize(self):
        pass