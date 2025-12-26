def list_activities(environ, start_response, module):
    session = module.get_db_session()()
    activity_service = module.env.get_service('activities_activity_service')
    activities = activity_service.list_activities(session)
    return module.response(start_response, {'activities': [a.__dict__ for a in activities]})

def create_activity(environ, start_response, module):
    body = module.get_body(environ)
    session = module.get_db_session()()
    activity_service = module.env.get_service('activities_activity_service')
    activity = activity_service.create_activity(session, body)
    module.emit_event('activity_created', {'activity_id': activity.id})
    return module.response(start_response, {'activity': activity.__dict__}, '201 Created')

def get_activity(environ, start_response, module):
    activity_id = environ['ROUTE_PARAMS']['id']
    session = module.get_db_session()()
    activity_service = module.env.get_service('activities_activity_service')
    activity = activity_service.get_activity(session, activity_id)
    if activity:
        return module.response(start_response, {'activity': activity.__dict__})
    return module.response(start_response, {'error': 'Activity not found'}, '404 Not Found')

def update_activity(environ, start_response, module):
    activity_id = environ['ROUTE_PARAMS']['id']
    body = module.get_body(environ)
    session = module.get_db_session()()
    activity_service = module.env.get_service('activities_activity_service')
    activity = activity_service.update_activity(session, activity_id, body)
    if activity:
        return module.response(start_response, {'activity': activity.__dict__})
    return module.response(start_response, {'error': 'Activity not found'}, '404 Not Found')

def log_call(environ, start_response, module):
    body = module.get_body(environ)
    session = module.get_db_session()()
    activity_service = module.env.get_service('activities_activity_service')
    call = activity_service.log_call(session, body)
    return module.response(start_response, {'call': call.__dict__}, '201 Created')

def log_meeting(environ, start_response, module):
    body = module.get_body(environ)
    session = module.get_db_session()()
    activity_service = module.env.get_service('activities_activity_service')
    meeting = activity_service.log_meeting(session, body)
    return module.response(start_response, {'meeting': meeting.__dict__}, '201 Created')
