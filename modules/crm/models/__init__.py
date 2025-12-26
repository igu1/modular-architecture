from database import Base
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from datetime import datetime

class Company(Base):
    __tablename__ = 'crm_companies'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    industry = Column(String(50))
    website = Column(String(200))
    phone = Column(String(20))
    email = Column(String(100))
    address = Column(Text)
    city = Column(String(50))
    state = Column(String(50))
    country = Column(String(50))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

