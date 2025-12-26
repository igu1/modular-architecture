from database import DatabaseModel, Base
from sqlalchemy import Column, Integer, String, DateTime, Text, Enum, ForeignKey
from datetime import datetime
import enum

class LeadStatus(enum.Enum):
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    CONVERTED = "converted"
    LOST = "lost"

class Lead(DatabaseModel):
    __tablename__ = 'leads'
    
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('crm_companies.id'), nullable=False)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    phone = Column(String(20))
    company = Column(String(100))
    status = Column(Enum(LeadStatus), default=LeadStatus.NEW)
    source = Column(String(50))
    notes = Column(Text)
    assigned_to = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
