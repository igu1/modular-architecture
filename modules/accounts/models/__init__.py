from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Float, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database import DatabaseModel, Base

class Account(DatabaseModel):
    __tablename__ = 'accounts'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    account_number = Column(String(50), unique=True)
    account_type = Column(String(50))
    industry = Column(String(100))
    website = Column(String(255))
    phone = Column(String(50))
    fax = Column(String(50))
    annual_revenue = Column(Float)
    number_of_employees = Column(Integer)
    ownership = Column(String(50))
    ticker_symbol = Column(String(20))
    rating = Column(String(50))
    sic_code = Column(String(20))
    billing_address_line1 = Column(String(255))
    billing_address_line2 = Column(String(255))
    billing_city = Column(String(100))
    billing_state = Column(String(100))
    billing_postal_code = Column(String(20))
    billing_country = Column(String(100))
    shipping_address_line1 = Column(String(255))
    shipping_address_line2 = Column(String(255))
    shipping_city = Column(String(100))
    shipping_state = Column(String(100))
    shipping_postal_code = Column(String(20))
    shipping_country = Column(String(100))
    parent_account_id = Column(Integer, ForeignKey('accounts.id'))
    status = Column(String(50), default='active')
    description = Column(Text)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(Integer, ForeignKey('users.id'))
    assigned_to = Column(Integer, ForeignKey('users.id'))
