class ActivityService:
    
    def __init__(self):
        self.name = "activity_service"
    
    def create_activity(self, session, activity_data):
        from modules.activities.models import Activity
        activity = Activity(**activity_data)
        session.add(activity)
        session.commit()
        return activity
    
    def get_activity(self, session, activity_id):
        from modules.activities.models import Activity
        return session.query(Activity).filter(Activity.id == activity_id).first()
    
    def update_activity(self, session, activity_id, activity_data):
        from modules.activities.models import Activity
        activity = session.query(Activity).filter(Activity.id == activity_id).first()
        if activity:
            for key, value in activity_data.items():
                setattr(activity, key, value)
            session.commit()
        return activity
    
    def list_activities(self, session, filters=None):
        from modules.activities.models import Activity
        query = session.query(Activity)
        if filters:
            for key, value in filters.items():
                query = query.filter(getattr(Activity, key) == value)
        return query.all()
    
    def log_call(self, session, call_data):
        from modules.activities.models import Call
        call = Call(**call_data)
        session.add(call)
        session.commit()
        return call
    
    def log_meeting(self, session, meeting_data):
        from modules.activities.models import Meeting
        meeting = Meeting(**meeting_data)
        session.add(meeting)
        session.commit()
        return meeting
