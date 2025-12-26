from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Float, Date, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Campaign(Base):
    __tablename__ = 'campaigns'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    campaign_type = Column(String(50))
    status = Column(String(50), default='planning')
    start_date = Column(Date)
    end_date = Column(Date)
    budget = Column(Float, default=0.0)
    actual_cost = Column(Float, default=0.0)
    expected_revenue = Column(Float, default=0.0)
    expected_response = Column(Integer, default=0)
    num_sent = Column(Integer, default=0)
    description = Column(Text)
    target_audience = Column(Text)
    objectives = Column(Text)
    notes = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(Integer, ForeignKey('users.id'))
    assigned_to = Column(Integer, ForeignKey('users.id'))

class CampaignMember(Base):
    __tablename__ = 'campaign_members'
    
    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, ForeignKey('campaigns.id'), nullable=False)
    contact_id = Column(Integer, ForeignKey('contacts.id'))
    lead_id = Column(Integer, ForeignKey('leads.id'))
    status = Column(String(50))
    response = Column(String(50))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
