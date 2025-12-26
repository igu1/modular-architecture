class EmailMarketingService:
    
    def __init__(self):
        self.name = "email_marketing_service"
    
    def create_template(self, session, template_data):
        from modules.email_marketing.models import EmailTemplate
        template = EmailTemplate(**template_data)
        session.add(template)
        session.commit()
        return template
    
    def create_email_campaign(self, session, campaign_data):
        from modules.email_marketing.models import EmailCampaign
        campaign = EmailCampaign(**campaign_data)
        session.add(campaign)
        session.commit()
        return campaign
    
    def track_email(self, session, tracking_data):
        from modules.email_marketing.models import EmailTracking
        tracking = EmailTracking(**tracking_data)
        session.add(tracking)
        session.commit()
        return tracking
    
    def list_templates(self, session, filters=None):
        from modules.email_marketing.models import EmailTemplate
        query = session.query(EmailTemplate)
        if filters:
            for key, value in filters.items():
                query = query.filter(getattr(EmailTemplate, key) == value)
        return query.all()
    
    def list_email_campaigns(self, session, filters=None):
        from modules.email_marketing.models import EmailCampaign
        query = session.query(EmailCampaign)
        if filters:
            for key, value in filters.items():
                query = query.filter(getattr(EmailCampaign, key) == value)
        return query.all()
