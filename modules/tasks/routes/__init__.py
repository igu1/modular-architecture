routes = [
    ('/api/tasks', 'GET', 'modules.tasks.views.tasks.list_tasks'),
    ('/api/tasks', 'POST', 'modules.tasks.views.tasks.create_task'),
    ('/api/tasks/<id>', 'GET', 'modules.tasks.views.tasks.get_task'),
    ('/api/tasks/<id>', 'PUT', 'modules.tasks.views.tasks.update_task'),
    ('/api/tasks/<id>', 'DELETE', 'modules.tasks.views.tasks.delete_task'),
]
