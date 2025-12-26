routes = [
    ('/api/activities', 'GET', 'modules.activities.views.activities.list_activities'),
    ('/api/activities', 'POST', 'modules.activities.views.activities.create_activity'),
    ('/api/activities/<id>', 'GET', 'modules.activities.views.activities.get_activity'),
    ('/api/activities/<id>', 'PUT', 'modules.activities.views.activities.update_activity'),
    ('/api/calls', 'POST', 'modules.activities.views.activities.log_call'),
    ('/api/meetings', 'POST', 'modules.activities.views.activities.log_meeting'),
]
