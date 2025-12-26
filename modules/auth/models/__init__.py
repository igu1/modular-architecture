from database import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)

class Session(Base):
    __tablename__ = 'auth_sessions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    session_token = Column(String(255), unique=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
