routes = [
    ('/api/notifications', 'GET', 'modules.notifications.views.notifications.list_notifications'),
    ('/api/notifications', 'POST', 'modules.notifications.views.notifications.create_notification'),
    ('/api/notifications/<id>/read', 'PUT', 'modules.notifications.views.notifications.mark_as_read'),
]
