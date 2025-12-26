class CampaignService:
    
    def __init__(self):
        self.name = "campaign_service"
    
    def create_campaign(self, session, campaign_data):
        from modules.campaigns.models import Campaign
        campaign = Campaign(**campaign_data)
        session.add(campaign)
        session.commit()
        return campaign
    
    def get_campaign(self, session, campaign_id):
        from modules.campaigns.models import Campaign
        return session.query(Campaign).filter(Campaign.id == campaign_id).first()
    
    def update_campaign(self, session, campaign_id, campaign_data):
        from modules.campaigns.models import Campaign
        campaign = session.query(Campaign).filter(Campaign.id == campaign_id).first()
        if campaign:
            for key, value in campaign_data.items():
                setattr(campaign, key, value)
            session.commit()
        return campaign
    
    def delete_campaign(self, session, campaign_id):
        from modules.campaigns.models import Campaign
        campaign = session.query(Campaign).filter(Campaign.id == campaign_id).first()
        if campaign:
            session.delete(campaign)
            session.commit()
            return True
        return False
    
    def list_campaigns(self, session, filters=None):
        from modules.campaigns.models import Campaign
        query = session.query(Campaign)
        if filters:
            for key, value in filters.items():
                query = query.filter(getattr(Campaign, key) == value)
        return query.all()
    
    def add_member(self, session, member_data):
        from modules.campaigns.models import CampaignMember
        member = CampaignMember(**member_data)
        session.add(member)
        session.commit()
        return member
