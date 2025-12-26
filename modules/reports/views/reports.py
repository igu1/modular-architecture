def list_reports(environ, start_response, module):
    session = module.get_db_session()()
    report_service = module.env.get_service('reports_report_service')
    reports = report_service.list_reports(session)
    return module.response(start_response, {'reports': [r.__dict__ for r in reports]})

def create_report(environ, start_response, module):
    body = module.get_body(environ)
    session = module.get_db_session()()
    report_service = module.env.get_service('reports_report_service')
    report = report_service.create_report(session, body)
    return module.response(start_response, {'report': report.__dict__}, '201 Created')

def get_report(environ, start_response, module):
    report_id = environ['ROUTE_PARAMS']['id']
    session = module.get_db_session()()
    report_service = module.env.get_service('reports_report_service')
    report = report_service.get_report(session, report_id)
    if report:
        return module.response(start_response, {'report': report.__dict__})
    return module.response(start_response, {'error': 'Report not found'}, '404 Not Found')

def schedule_report(environ, start_response, module):
    report_id = environ['ROUTE_PARAMS']['id']
    body = module.get_body(environ)
    body['report_id'] = report_id
    session = module.get_db_session()()
    report_service = module.env.get_service('reports_report_service')
    schedule = report_service.schedule_report(session, body)
    return module.response(start_response, {'schedule': schedule.__dict__}, '201 Created')
