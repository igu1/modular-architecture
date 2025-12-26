from modules.engine import BaseModule

class KnowledgeBase(BaseModule):
    dependencies = ['base']
    
    def __init__(self):
        super().__init__()

    def initialize(self, env):
        super().initialize(env)
        self.subscribe_to_event('ticket_resolved', self.on_ticket_resolved)
        self.log("Knowledge Base module initialized", "info")

    def on_ticket_resolved(self, event_data):
        self.log(f"Ticket resolved - consider adding to knowledge base: {event_data}", "info")

    def load_routes(self):
        return super().load_routes()

    def deinitialize(self):
        pass
