from .base import Base
from .auth import Auth
from .crm import CRM
from .leads import Leads
from .customers import Customers
from .newsletter import Newsletter

# Core CRM modules
from .contacts import Contacts
from .accounts import Accounts
from .opportunities import Opportunities

# Sales modules
from .products import Products
from .quotes import Quotes
from .orders import Orders
from .invoices import Invoices

# Marketing modules
from .campaigns import Campaigns
from .email_marketing import EmailMarketing

# Support modules
from .tickets import Tickets
from .knowledge_base import KnowledgeBase

# Automation modules
from .tasks import Tasks
from .workflows import Workflows
from .notifications import Notifications

# Communication modules
from .activities import Activities

# Analytics modules
from .reports import Reports
from .dashboards import Dashboards

modules = {
    'base': Base,
    'auth': Auth,
    'crm': CRM,
    'leads': Leads,
    'customers': Customers,
    'newsletter': Newsletter,
    'contacts': Contacts,
    'accounts': Accounts,
    'opportunities': Opportunities,
    'products': Products,
    'quotes': Quotes,
    'orders': Orders,
    'invoices': Invoices,
    'campaigns': Campaigns,
    'email_marketing': EmailMarketing,
    'tickets': Tickets,
    'knowledge_base': KnowledgeBase,
    'tasks': Tasks,
    'workflows': Workflows,
    'notifications': Notifications,
    'activities': Activities,
    'reports': Reports,
    'dashboards': Dashboards
}

__all__ = ["modules"]