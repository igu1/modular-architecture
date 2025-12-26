from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Report(Base):
    __tablename__ = 'reports'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    report_type = Column(String(50))
    module_name = Column(String(50))
    query_config = Column(JSON)
    filters = Column(JSON)
    columns = Column(JSON)
    is_public = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(Integer, ForeignKey('users.id'))

class ReportSchedule(Base):
    __tablename__ = 'report_schedules'
    
    id = Column(Integer, primary_key=True)
    report_id = Column(Integer, ForeignKey('reports.id'), nullable=False)
    schedule_type = Column(String(50))
    schedule_config = Column(JSON)
    recipients = Column(JSON)
    is_active = Column(Boolean, default=True)
    last_run_at = Column(DateTime)
    next_run_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
