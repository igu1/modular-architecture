from database import init_db, get_session

class DatabaseService:
    def __init__(self):
        # Initialize database if not already done
        try:
            init_db("sqlite:///test.db")
        except Exception as e:
            print(f"Database already initialized or error: {e}")
    
    def get_session(self):
        """Get database session function"""
        return get_session
    
    def init_database(self, db_url="sqlite:///test.db"):
        """Initialize database with custom URL"""
        return init_db(db_url)
    
    def health_check(self):
        """Check database connectivity"""
        try:
            session_func = self.get_session()
            session = session_func()
            session.execute("SELECT 1")
            return {"status": "healthy", "message": "Database connection successful"}
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}
