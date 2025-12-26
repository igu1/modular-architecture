routes = [
    ('/api/dashboards', 'GET', 'modules.dashboards.views.dashboards.list_dashboards'),
    ('/api/dashboards', 'POST', 'modules.dashboards.views.dashboards.create_dashboard'),
    ('/api/dashboards/<id>', 'GET', 'modules.dashboards.views.dashboards.get_dashboard'),
    ('/api/dashboards/<id>/widgets', 'POST', 'modules.dashboards.views.dashboards.add_widget'),
]
