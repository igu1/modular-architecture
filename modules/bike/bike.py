
class Bike:
    def initialize(self, db_conn, shared_context):
        print("Initializing Generic Bike...")
        self.db_conn = db_conn
        self.shared_context = shared_context
        self.shared_context['event_dispatcher']['on']('bike_create', self.on_bike_create)
        self.shared_context['event_dispatcher']['on']('bike_list', self.on_bike_list)
        return self

    def get_bikes(self):
        # This is a placeholder - in a real implementation, this would query the bike database
        return [{"id": 1, "name": "Mountain Bike"}, {"id": 2, "name": "Road Bike"}]

    def deinitialize(self):
        print("Deinitializing Generic Bike...")
        if hasattr(self, 'db_conn') and self.db_conn:
            try:
                self.db_conn.close()
            except Exception as e:
                print(f"Error closing database connection for Bike: {e}")
            finally:
                self.db_conn = None
    
    def on_bike_create(self, payload, context):
        print(f"Bike module received create event: {payload}")

    def on_bike_list(self, payload, context):
        print(f"Bike module received list event: {payload}")
        bikes = self.get_bikes()
        print(f"Bike list: {bikes}")
        return bikes