
from modules.base import BaseModule

class Car(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "Generic Car"
    
    def initialize(self, db_conn, shared_context):
        print(f"Initializing {self.name} with database...")
        self.db_conn = db_conn
        self.shared_context = shared_context
        self.create_cars()
        return self

    def deinitialize(self):
        try:
            if hasattr(self, 'db_conn') and self.db_conn:
                cursor = self.db_conn.cursor()
                cursor.execute("DELETE FROM cars")
                self.db_conn.commit()
                cursor.close()
                self.db_conn.close()
                print(f"Deinitialized {self.name} database connection")
        except Exception as e:
            print(f"Error during deinitialization of {self.name}: {e}")
            raise
        finally:
            return self
        
    def create_cars(self) -> bool:
        try:
            print("Creating cars...")
            cursor = self.db_conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS cars
                            (id INTEGER PRIMARY KEY, make TEXT, model TEXT)''')
            self.db_conn.commit()
            print("Cars table created successfully")
            cursor.execute("INSERT INTO cars (make, model) VALUES (?, ?)", ("Toyota", "Camry"))
            self.db_conn.commit()
            print("Sample car inserted successfully")
            cursor.close()
            print("Car module operations completed successfully")
            return True
        except Exception as e:
            print(f"Error in car module: {e}")
            return False
    
    def get_cars_count(self) -> int:
        try:
            cursor = self.db_conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM cars")
            count = cursor.fetchone()[0]
            cursor.close()
            return count
        except Exception as e:
            print(f"Error getting cars count: {e}")
            return 0
    
    def get_cars(self):
        try:
            cursor = self.db_conn.cursor()
            cursor.execute("SELECT * FROM cars")
            cars = cursor.fetchall()
            cursor.close()
            return cars
        except Exception as e:
            print(f"Error getting cars: {e}")
            return []
    
    def get_bikes(self):
        loaded_modules = self.shared_context.get('loaded_modules', {})
        bike_module = loaded_modules.get('bike')
        if bike_module and hasattr(bike_module, 'get_bikes'):
            return bike_module.get_bikes()
        return None