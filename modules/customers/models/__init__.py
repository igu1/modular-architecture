from database import DatabaseModel, Base
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey
from datetime import datetime

class Customer(DatabaseModel):
    __tablename__ = 'customers'
    
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('crm_companies.id'), nullable=False)
    lead_id = Column(Integer, ForeignKey('leads.id'), nullable=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    phone = Column(String(20))
    company = Column(String(100))
    address = Column(Text)
    city = Column(String(50))
    country = Column(String(50))
    is_active = Column(Boolean, default=True)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
