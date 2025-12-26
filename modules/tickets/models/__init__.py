from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Ticket(Base):
    __tablename__ = 'tickets'
    
    id = Column(Integer, primary_key=True)
    ticket_number = Column(String(50), unique=True, nullable=False)
    subject = Column(String(500), nullable=False)
    description = Column(Text)
    status = Column(String(50), default='new')
    priority = Column(String(50), default='medium')
    category = Column(String(100))
    account_id = Column(Integer, ForeignKey('accounts.id'))
    contact_id = Column(Integer, ForeignKey('contacts.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    assigned_to = Column(Integer, ForeignKey('users.id'))
    source = Column(String(50))
    resolution = Column(Text)
    resolved_at = Column(DateTime)
    closed_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(Integer, ForeignKey('users.id'))

class TicketComment(Base):
    __tablename__ = 'ticket_comments'
    
    id = Column(Integer, primary_key=True)
    ticket_id = Column(Integer, ForeignKey('tickets.id'), nullable=False)
    comment = Column(Text, nullable=False)
    is_internal = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(Integer, ForeignKey('users.id'))
