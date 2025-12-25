from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Optional, List, Dict, Any

_engine = None
_SessionLocal = None
Base = declarative_base()

def init_db(database_url: str = "sqlite:///test.db"):
    """Initialize database - call once at startup"""
    global _engine, _SessionLocal
    _engine = create_engine(database_url)
    _SessionLocal = sessionmaker(bind=_engine)
    Base.metadata.create_all(bind=_engine)

def get_session():
    """Get database session"""
    if not _SessionLocal:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    return _SessionLocal()

class DatabaseModel(Base):
    """Base model class with Django-like methods"""
    __abstract__ = True
    
    @classmethod
    def create(cls, **kwargs):
        """Create new record"""
        with get_session() as session:
            instance = cls(**kwargs)
            session.add(instance)
            session.commit()
            session.refresh(instance)
            return instance
    
    @classmethod
    def get(cls, **kwargs):
        """Get first matching record"""
        with get_session() as session:
            return session.query(cls).filter_by(**kwargs).first()
    
    @classmethod
    def filter(cls, **kwargs):
        """Get all matching records"""
        with get_session() as session:
            return session.query(cls).filter_by(**kwargs).all()
    
    @classmethod
    def all(cls):
        """Get all records"""
        with get_session() as session:
            return session.query(cls).all()
    
    @classmethod
    def count(cls):
        """Count all records"""
        with get_session() as session:
            return session.query(cls).count()
    
    def update(self, **kwargs):
        """Update record"""
        with get_session() as session:
            for key, value in kwargs.items():
                if hasattr(self, key):
                    setattr(self, key, value)
            session.merge(self)
            session.commit()
            session.refresh(self)
            return self
    
    def delete(self):
        """Delete record"""
        with get_session() as session:
            session.delete(self)
            session.commit()
            return True
    
    def to_dict(self):
        """Convert to dictionary"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
