from .base import Base
from .auth import Auth
from .restaurant import Restaurant

modules = {
    'base': Base,
    'auth': Auth,
    'restaurant': Restaurant
}

__all__ = ["modules"]