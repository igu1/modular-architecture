def list_dashboards(environ, start_response, module):
    session = module.get_db_session()()
    dashboard_service = module.env.get_service('dashboards_dashboard_service')
    dashboards = dashboard_service.list_dashboards(session)
    return module.response(start_response, {'dashboards': [d.__dict__ for d in dashboards]})

def create_dashboard(environ, start_response, module):
    body = module.get_body(environ)
    session = module.get_db_session()()
    dashboard_service = module.env.get_service('dashboards_dashboard_service')
    dashboard = dashboard_service.create_dashboard(session, body)
    return module.response(start_response, {'dashboard': dashboard.__dict__}, '201 Created')

def get_dashboard(environ, start_response, module):
    dashboard_id = environ['ROUTE_PARAMS']['id']
    session = module.get_db_session()()
    dashboard_service = module.env.get_service('dashboards_dashboard_service')
    dashboard = dashboard_service.get_dashboard(session, dashboard_id)
    if dashboard:
        return module.response(start_response, {'dashboard': dashboard.__dict__})
    return module.response(start_response, {'error': 'Dashboard not found'}, '404 Not Found')

def add_widget(environ, start_response, module):
    dashboard_id = environ['ROUTE_PARAMS']['id']
    body = module.get_body(environ)
    body['dashboard_id'] = dashboard_id
    session = module.get_db_session()()
    dashboard_service = module.env.get_service('dashboards_dashboard_service')
    widget = dashboard_service.add_widget(session, body)
    return module.response(start_response, {'widget': widget.__dict__}, '201 Created')
