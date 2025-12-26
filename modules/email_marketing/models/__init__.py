from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class EmailTemplate(Base):
    __tablename__ = 'email_templates'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    subject = Column(String(500))
    body_html = Column(Text)
    body_text = Column(Text)
    template_type = Column(String(50))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(Integer, ForeignKey('users.id'))

class EmailCampaign(Base):
    __tablename__ = 'email_campaigns'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    campaign_id = Column(Integer, ForeignKey('campaigns.id'))
    template_id = Column(Integer, ForeignKey('email_templates.id'))
    subject = Column(String(500))
    from_email = Column(String(255))
    from_name = Column(String(255))
    status = Column(String(50), default='draft')
    scheduled_at = Column(DateTime)
    sent_at = Column(DateTime)
    total_recipients = Column(Integer, default=0)
    total_sent = Column(Integer, default=0)
    total_delivered = Column(Integer, default=0)
    total_opened = Column(Integer, default=0)
    total_clicked = Column(Integer, default=0)
    total_bounced = Column(Integer, default=0)
    total_unsubscribed = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(Integer, ForeignKey('users.id'))

class EmailTracking(Base):
    __tablename__ = 'email_tracking'
    
    id = Column(Integer, primary_key=True)
    email_campaign_id = Column(Integer, ForeignKey('email_campaigns.id'))
    contact_id = Column(Integer, ForeignKey('contacts.id'))
    email = Column(String(255))
    status = Column(String(50))
    sent_at = Column(DateTime)
    opened_at = Column(DateTime)
    clicked_at = Column(DateTime)
    bounced_at = Column(DateTime)
    unsubscribed_at = Column(DateTime)
    open_count = Column(Integer, default=0)
    click_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
