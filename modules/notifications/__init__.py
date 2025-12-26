from modules.engine import BaseModule

class Notifications(BaseModule):
    dependencies = ['base']
    
    def __init__(self):
        super().__init__()

    def initialize(self, env):
        super().initialize(env)
        self.subscribe_to_event('task_created', self.on_task_created)
        self.subscribe_to_event('ticket_created', self.on_ticket_created)
        self.log("Notifications module initialized", "info")

    def on_task_created(self, event_data):
        self.log(f"Task created - sending notification: {event_data}", "info")
    
    def on_ticket_created(self, event_data):
        self.log(f"Ticket created - sending notification: {event_data}", "info")

    def load_routes(self):
        return super().load_routes()

    def deinitialize(self):
        pass
