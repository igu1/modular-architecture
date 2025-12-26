routes = [
    ('/leads', 'GET', 'modules.leads.views.leads.list_leads'),
    ('/leads', 'POST', 'modules.leads.views.leads.create_lead'),
    ('/leads/<id>', 'GET', 'modules.leads.views.leads.get_lead'),
    ('/leads/<id>', 'PUT', 'modules.leads.views.leads.update_lead'),
    ('/leads/<id>', 'DELETE', 'modules.leads.views.leads.delete_lead'),
    ('/leads/<id>/convert', 'POST', 'modules.leads.views.leads.convert_lead'),
]
