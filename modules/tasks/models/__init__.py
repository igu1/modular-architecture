from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Date, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Task(Base):
    __tablename__ = 'tasks'
    
    id = Column(Integer, primary_key=True)
    subject = Column(String(500), nullable=False)
    description = Column(Text)
    status = Column(String(50), default='not_started')
    priority = Column(String(50), default='normal')
    due_date = Column(Date)
    reminder_date = Column(DateTime)
    related_to_type = Column(String(50))
    related_to_id = Column(Integer)
    account_id = Column(Integer, ForeignKey('accounts.id'))
    contact_id = Column(Integer, ForeignKey('contacts.id'))
    opportunity_id = Column(Integer, ForeignKey('opportunities.id'))
    assigned_to = Column(Integer, ForeignKey('users.id'))
    completed_at = Column(DateTime)
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(Integer, ForeignKey('users.id'))
