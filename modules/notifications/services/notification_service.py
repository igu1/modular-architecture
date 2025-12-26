class NotificationService:
    
    def __init__(self):
        self.name = "notification_service"
    
    def create_notification(self, session, notification_data):
        from modules.notifications.models import Notification
        notification = Notification(**notification_data)
        session.add(notification)
        session.commit()
        return notification
    
    def get_user_notifications(self, session, user_id, unread_only=False):
        from modules.notifications.models import Notification
        query = session.query(Notification).filter(Notification.user_id == user_id)
        if unread_only:
            query = query.filter(Notification.is_read == False)
        return query.all()
    
    def mark_as_read(self, session, notification_id):
        from modules.notifications.models import Notification
        from datetime import datetime
        notification = session.query(Notification).filter(Notification.id == notification_id).first()
        if notification:
            notification.is_read = True
            notification.read_at = datetime.utcnow()
            session.commit()
        return notification
