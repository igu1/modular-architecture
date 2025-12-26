from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class KBArticle(Base):
    __tablename__ = 'kb_articles'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(500), nullable=False)
    content = Column(Text, nullable=False)
    summary = Column(Text)
    category_id = Column(Integer, ForeignKey('kb_categories.id'))
    status = Column(String(50), default='draft')
    is_published = Column(Boolean, default=False)
    view_count = Column(Integer, default=0)
    helpful_count = Column(Integer, default=0)
    not_helpful_count = Column(Integer, default=0)
    tags = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = Column(DateTime)
    created_by = Column(Integer, ForeignKey('users.id'))
    updated_by = Column(Integer, ForeignKey('users.id'))

class KBCategory(Base):
    __tablename__ = 'kb_categories'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    parent_id = Column(Integer, ForeignKey('kb_categories.id'))
    display_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
