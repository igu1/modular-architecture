from modules.engine import BaseModule

class Base(BaseModule):
    
    def __init__(self):
        super().__init__()

    def initialize(self, db_conn, shared_context):
        super().initialize(db_conn, shared_context)

    def load_routes(self):
        return super().load_routes()

    def deinitialize(self):
        pass