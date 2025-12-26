from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Workflow(Base):
    __tablename__ = 'workflows'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    trigger_type = Column(String(50))
    trigger_object = Column(String(50))
    trigger_conditions = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(Integer, ForeignKey('users.id'))

class WorkflowAction(Base):
    __tablename__ = 'workflow_actions'
    
    id = Column(Integer, primary_key=True)
    workflow_id = Column(Integer, ForeignKey('workflows.id'), nullable=False)
    action_type = Column(String(50), nullable=False)
    action_config = Column(JSON)
    execution_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

class WorkflowExecution(Base):
    __tablename__ = 'workflow_executions'
    
    id = Column(Integer, primary_key=True)
    workflow_id = Column(Integer, ForeignKey('workflows.id'), nullable=False)
    status = Column(String(50))
    trigger_data = Column(JSON)
    execution_log = Column(Text)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
