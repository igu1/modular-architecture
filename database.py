from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Optional, List, Dict, Any
from contextlib import contextmanager

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


# Manassilakkanund
@contextmanager
def session_scope(commit=True):
    session = get_session()
    try:
        yield session
        if commit:
            session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

class DatabaseModel(Base):
    __abstract__ = True
    
    @classmethod
    def create(cls, **kwargs):
        with session_scope() as session:
            instance = cls(**kwargs)
            session.add(instance)
            session.flush()
            session.refresh(instance)
            return instance.to_dict()
    
    @classmethod
    def get(cls, **kwargs):
        with session_scope(commit=False) as session:
            instance = session.query(cls).filter_by(**kwargs).first()
            return instance.to_dict() if instance else None
    
    @classmethod
    def filter(cls, **kwargs):
        with session_scope(commit=False) as session:
            instances = session.query(cls).filter_by(**kwargs).all()
            return [inst.to_dict() for inst in instances]
    
    @classmethod
    def all(cls):
        with session_scope(commit=False) as session:
            instances = session.query(cls).all()
            return [inst.to_dict() for inst in instances]
    
    @classmethod
    def count(cls):
        with session_scope(commit=False) as session:
            return session.query(cls).count()
    
    @classmethod
    def update_record(cls, record_id, **kwargs):
        with session_scope() as session:
            instance = session.query(cls).filter_by(id=record_id).first()
            if instance:
                for key, value in kwargs.items():
                    if hasattr(instance, key):
                        setattr(instance, key, value)
                session.flush()
                session.refresh(instance)
                return instance.to_dict()
            return None
    
    @classmethod
    def delete_record(cls, record_id):
        with session_scope() as session:
            instance = session.query(cls).filter_by(id=record_id).first()
            if instance:
                session.delete(instance)
                return True
            return False
    
    def to_dict(self):
        result = {}
        for c in self.__table__.columns:
            value = getattr(self, c.name)
            if hasattr(value, 'isoformat'):
                value = value.isoformat()
            elif hasattr(value, 'value'):
                value = value.value
            result[c.name] = value
        return result
