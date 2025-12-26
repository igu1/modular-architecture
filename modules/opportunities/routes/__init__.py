routes = [
    ('/api/opportunities', 'GET', 'modules.opportunities.views.opportunities.list_opportunities'),
    ('/api/opportunities', 'POST', 'modules.opportunities.views.opportunities.create_opportunity'),
    ('/api/opportunities/<id>', 'GET', 'modules.opportunities.views.opportunities.get_opportunity'),
    ('/api/opportunities/<id>', 'PUT', 'modules.opportunities.views.opportunities.update_opportunity'),
    ('/api/opportunities/<id>', 'DELETE', 'modules.opportunities.views.opportunities.delete_opportunity'),
    ('/api/opportunities/pipeline', 'GET', 'modules.opportunities.views.opportunities.get_pipeline'),
]
