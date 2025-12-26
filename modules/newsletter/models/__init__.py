from database import DatabaseModel, Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from datetime import datetime

class Subscriber(DatabaseModel):
    __tablename__ = 'newsletter_subscribers'
    
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('crm_companies.id'), nullable=False)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=True)
    email = Column(String(100), nullable=False)
    name = Column(String(100))
    is_active = Column(Boolean, default=True)
    subscribed_at = Column(DateTime, default=datetime.utcnow)
    unsubscribed_at = Column(DateTime)

class Campaign(DatabaseModel):
    __tablename__ = 'newsletter_campaigns'
    
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('crm_companies.id'), nullable=False)
    name = Column(String(100), nullable=False)
    subject = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    status = Column(String(20), default='draft')
    sent_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(Integer)
