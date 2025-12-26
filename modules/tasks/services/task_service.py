class TaskService:
    
    def __init__(self):
        self.name = "task_service"
    
    def create_task(self, session, task_data):
        from modules.tasks.models import Task
        task = Task(**task_data)
        session.add(task)
        session.commit()
        return task
    
    def get_task(self, session, task_id):
        from modules.tasks.models import Task
        return session.query(Task).filter(Task.id == task_id).first()
    
    def update_task(self, session, task_id, task_data):
        from modules.tasks.models import Task
        task = session.query(Task).filter(Task.id == task_id).first()
        if task:
            for key, value in task_data.items():
                setattr(task, key, value)
            session.commit()
        return task
    
    def delete_task(self, session, task_id):
        from modules.tasks.models import Task
        task = session.query(Task).filter(Task.id == task_id).first()
        if task:
            session.delete(task)
            session.commit()
            return True
        return False
    
    def list_tasks(self, session, filters=None):
        from modules.tasks.models import Task
        query = session.query(Task)
        if filters:
            for key, value in filters.items():
                query = query.filter(getattr(Task, key) == value)
        return query.all()
