from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Float, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Quote(Base):
    __tablename__ = 'quotes'
    
    id = Column(Integer, primary_key=True)
    quote_number = Column(String(50), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    opportunity_id = Column(Integer, ForeignKey('opportunities.id'))
    account_id = Column(Integer, ForeignKey('accounts.id'))
    contact_id = Column(Integer, ForeignKey('contacts.id'))
    status = Column(String(50), default='draft')
    valid_until = Column(Date)
    subtotal = Column(Float, default=0.0)
    discount = Column(Float, default=0.0)
    tax = Column(Float, default=0.0)
    total_amount = Column(Float, default=0.0)
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
    terms_and_conditions = Column(Text)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(Integer, ForeignKey('users.id'))
    assigned_to = Column(Integer, ForeignKey('users.id'))

class QuoteLineItem(Base):
    __tablename__ = 'quote_line_items'
    
    id = Column(Integer, primary_key=True)
    quote_id = Column(Integer, ForeignKey('quotes.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'))
    description = Column(Text)
    quantity = Column(Float, default=1.0)
    unit_price = Column(Float)
    discount = Column(Float, default=0.0)
    tax = Column(Float, default=0.0)
    total_price = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
