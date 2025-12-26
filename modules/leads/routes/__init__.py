routes = [
    ('/api/leads', 'GET', 'modules.leads.views.leads.list_leads'),
    ('/api/leads', 'POST', 'modules.leads.views.leads.create_lead'),
    ('/api/leads/<id>', 'GET', 'modules.leads.views.leads.get_lead'),
    ('/api/leads/<id>', 'PUT', 'modules.leads.views.leads.update_lead'),
    ('/api/leads/<id>', 'DELETE', 'modules.leads.views.leads.delete_lead'),
    ('/api/leads/<id>/convert', 'POST', 'modules.leads.views.leads.convert_lead'),
]
