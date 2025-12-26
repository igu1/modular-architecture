class OpportunityService:
    
    def __init__(self):
        self.name = "opportunity_service"
    
    def create_opportunity(self, session, opportunity_data):
        from modules.opportunities.models import Opportunity
        opportunity = Opportunity(**opportunity_data)
        session.add(opportunity)
        session.commit()
        return opportunity
    
    def get_opportunity(self, session, opportunity_id):
        from modules.opportunities.models import Opportunity
        return session.query(Opportunity).filter(Opportunity.id == opportunity_id).first()
    
    def update_opportunity(self, session, opportunity_id, opportunity_data):
        from modules.opportunities.models import Opportunity
        opportunity = session.query(Opportunity).filter(Opportunity.id == opportunity_id).first()
        if opportunity:
            for key, value in opportunity_data.items():
                setattr(opportunity, key, value)
            session.commit()
        return opportunity
    
    def delete_opportunity(self, session, opportunity_id):
        from modules.opportunities.models import Opportunity
        opportunity = session.query(Opportunity).filter(Opportunity.id == opportunity_id).first()
        if opportunity:
            session.delete(opportunity)
            session.commit()
            return True
        return False
    
    def list_opportunities(self, session, filters=None):
        from modules.opportunities.models import Opportunity
        query = session.query(Opportunity)
        if filters:
            for key, value in filters.items():
                query = query.filter(getattr(Opportunity, key) == value)
        return query.all()
    
    def get_pipeline(self, session, user_id=None):
        from modules.opportunities.models import Opportunity
        query = session.query(Opportunity).filter(Opportunity.is_closed == 0)
        if user_id:
            query = query.filter(Opportunity.assigned_to == user_id)
        return query.all()
