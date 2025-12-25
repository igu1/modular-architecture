from modules.engine import BaseModule

class Base(BaseModule):
    
    def __init__(self):
        super().__init__()

    def initialize(self, db_conn, shared_context):
        return super().initialize(db_conn, shared_context)

    def deinitialize(self):
        pass