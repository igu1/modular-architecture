class WorkflowService:
    
    def __init__(self):
        self.name = "workflow_service"
    
    def create_workflow(self, session, workflow_data):
        from modules.workflows.models import Workflow
        workflow = Workflow(**workflow_data)
        session.add(workflow)
        session.commit()
        return workflow
    
    def get_workflow(self, session, workflow_id):
        from modules.workflows.models import Workflow
        return session.query(Workflow).filter(Workflow.id == workflow_id).first()
    
    def list_workflows(self, session, filters=None):
        from modules.workflows.models import Workflow
        query = session.query(Workflow)
        if filters:
            for key, value in filters.items():
                query = query.filter(getattr(Workflow, key) == value)
        return query.all()
    
    def add_action(self, session, action_data):
        from modules.workflows.models import WorkflowAction
        action = WorkflowAction(**action_data)
        session.add(action)
        session.commit()
        return action
