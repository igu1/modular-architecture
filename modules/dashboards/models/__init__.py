from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Dashboard(Base):
    __tablename__ = 'dashboards'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    layout_config = Column(JSON)
    is_default = Column(Boolean, default=False)
    is_public = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(Integer, ForeignKey('users.id'))

class DashboardWidget(Base):
    __tablename__ = 'dashboard_widgets'
    
    id = Column(Integer, primary_key=True)
    dashboard_id = Column(Integer, ForeignKey('dashboards.id'), nullable=False)
    widget_type = Column(String(50), nullable=False)
    title = Column(String(255))
    config = Column(JSON)
    position_x = Column(Integer, default=0)
    position_y = Column(Integer, default=0)
    width = Column(Integer, default=1)
    height = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
