from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Activity(Base):
    __tablename__ = 'activities'
    
    id = Column(Integer, primary_key=True)
    subject = Column(String(500), nullable=False)
    activity_type = Column(String(50), nullable=False)
    description = Column(Text)
    status = Column(String(50), default='planned')
    priority = Column(String(50), default='normal')
    activity_date = Column(DateTime)
    duration_minutes = Column(Integer)
    location = Column(String(255))
    related_to_type = Column(String(50))
    related_to_id = Column(Integer)
    account_id = Column(Integer, ForeignKey('accounts.id'))
    contact_id = Column(Integer, ForeignKey('contacts.id'))
    opportunity_id = Column(Integer, ForeignKey('opportunities.id'))
    assigned_to = Column(Integer, ForeignKey('users.id'))
    outcome = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(Integer, ForeignKey('users.id'))

class Call(Base):
    __tablename__ = 'calls'
    
    id = Column(Integer, primary_key=True)
    activity_id = Column(Integer, ForeignKey('activities.id'))
    call_type = Column(String(50))
    call_direction = Column(String(50))
    phone_number = Column(String(50))
    call_duration = Column(Integer)
    call_result = Column(String(100))
    recording_url = Column(String(500))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class Meeting(Base):
    __tablename__ = 'meetings'
    
    id = Column(Integer, primary_key=True)
    activity_id = Column(Integer, ForeignKey('activities.id'))
    meeting_type = Column(String(50))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    location = Column(String(255))
    meeting_url = Column(String(500))
    attendees = Column(Text)
    agenda = Column(Text)
    minutes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
