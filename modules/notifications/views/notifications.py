def list_notifications(environ, start_response, module):
    params = module.get_params(environ)
    user_id = params.get('user_id')
    unread_only = params.get('unread_only', 'false').lower() == 'true'
    session = module.get_db_session()()
    notification_service = module.env.get_service('notifications_notification_service')
    notifications = notification_service.get_user_notifications(session, user_id, unread_only)
    return module.response(start_response, {'notifications': [n.__dict__ for n in notifications]})

def create_notification(environ, start_response, module):
    body = module.get_body(environ)
    session = module.get_db_session()()
    notification_service = module.env.get_service('notifications_notification_service')
    notification = notification_service.create_notification(session, body)
    return module.response(start_response, {'notification': notification.__dict__}, '201 Created')

def mark_as_read(environ, start_response, module):
    notification_id = environ['ROUTE_PARAMS']['id']
    session = module.get_db_session()()
    notification_service = module.env.get_service('notifications_notification_service')
    notification = notification_service.mark_as_read(session, notification_id)
    if notification:
        return module.response(start_response, {'notification': notification.__dict__})
    return module.response(start_response, {'error': 'Notification not found'}, '404 Not Found')
