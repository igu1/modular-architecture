from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Float, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    product_code = Column(String(50), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    category = Column(String(100))
    product_type = Column(String(50))
    unit_price = Column(Float)
    cost_price = Column(Float)
    quantity_in_stock = Column(Integer, default=0)
    reorder_level = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    tax_rate = Column(Float, default=0.0)
    manufacturer = Column(String(255))
    supplier = Column(String(255))
    sku = Column(String(100))
    barcode = Column(String(100))
    weight = Column(Float)
    dimensions = Column(String(100))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(Integer, ForeignKey('users.id'))
