from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Float, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Opportunity(Base):
    __tablename__ = 'opportunities'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    account_id = Column(Integer, ForeignKey('accounts.id'))
    contact_id = Column(Integer, ForeignKey('contacts.id'))
    amount = Column(Float)
    close_date = Column(Date)
    stage = Column(String(50), nullable=False)
    probability = Column(Integer)
    type = Column(String(50))
    lead_source = Column(String(100))
    next_step = Column(String(255))
    forecast_category = Column(String(50))
    campaign_id = Column(Integer, ForeignKey('campaigns.id'))
    description = Column(Text)
    notes = Column(Text)
    is_closed = Column(Integer, default=0)
    is_won = Column(Integer, default=0)
    loss_reason = Column(String(255))
    competitor = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(Integer, ForeignKey('users.id'))
    assigned_to = Column(Integer, ForeignKey('users.id'))
