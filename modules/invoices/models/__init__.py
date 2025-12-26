from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Float, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Invoice(Base):
    __tablename__ = 'invoices'
    
    id = Column(Integer, primary_key=True)
    invoice_number = Column(String(50), unique=True, nullable=False)
    order_id = Column(Integer, ForeignKey('orders.id'))
    account_id = Column(Integer, ForeignKey('accounts.id'))
    contact_id = Column(Integer, ForeignKey('contacts.id'))
    status = Column(String(50), default='draft')
    invoice_date = Column(Date)
    due_date = Column(Date)
    subtotal = Column(Float, default=0.0)
    discount = Column(Float, default=0.0)
    tax = Column(Float, default=0.0)
    total_amount = Column(Float, default=0.0)
    amount_paid = Column(Float, default=0.0)
    amount_due = Column(Float, default=0.0)
    billing_address_line1 = Column(String(255))
    billing_address_line2 = Column(String(255))
    billing_city = Column(String(100))
    billing_state = Column(String(100))
    billing_postal_code = Column(String(20))
    billing_country = Column(String(100))
    payment_terms = Column(String(100))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(Integer, ForeignKey('users.id'))

class InvoiceLineItem(Base):
    __tablename__ = 'invoice_line_items'
    
    id = Column(Integer, primary_key=True)
    invoice_id = Column(Integer, ForeignKey('invoices.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'))
    description = Column(Text)
    quantity = Column(Float, default=1.0)
    unit_price = Column(Float)
    discount = Column(Float, default=0.0)
    tax = Column(Float, default=0.0)
    total_price = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

class Payment(Base):
    __tablename__ = 'payments'
    
    id = Column(Integer, primary_key=True)
    invoice_id = Column(Integer, ForeignKey('invoices.id'), nullable=False)
    payment_date = Column(Date)
    amount = Column(Float)
    payment_method = Column(String(50))
    transaction_id = Column(String(100))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(Integer, ForeignKey('users.id'))
