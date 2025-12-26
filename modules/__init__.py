from .base import Base
from .auth import Auth
from .crm import CRM
from .leads import Leads
from .customers import Customers
from .newsletter import Newsletter

modules = {
    'base': Base,
    'auth': Auth,
    'crm': CRM,
    'leads': Leads,
    'customers': Customers,
    'newsletter': Newsletter
}

__all__ = ["modules"]