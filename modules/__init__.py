from .base import Base
from .auth import Auth

modules = {
    'base': Base,
    'auth': Auth
}

__all__ = ["modules"]