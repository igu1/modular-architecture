def list_tasks(environ, start_response, module):
    session = module.get_db_session()()
    task_service = module.env.get_service('tasks_task_service')
    tasks = task_service.list_tasks(session)
    return module.response(start_response, {'tasks': [t.__dict__ for t in tasks]})

def create_task(environ, start_response, module):
    body = module.get_body(environ)
    session = module.get_db_session()()
    task_service = module.env.get_service('tasks_task_service')
    task = task_service.create_task(session, body)
    module.emit_event('task_created', {'task_id': task.id})
    return module.response(start_response, {'task': task.__dict__}, '201 Created')

def get_task(environ, start_response, module):
    task_id = environ['ROUTE_PARAMS']['id']
    session = module.get_db_session()()
    task_service = module.env.get_service('tasks_task_service')
    task = task_service.get_task(session, task_id)
    if task:
        return module.response(start_response, {'task': task.__dict__})
    return module.response(start_response, {'error': 'Task not found'}, '404 Not Found')

def update_task(environ, start_response, module):
    task_id = environ['ROUTE_PARAMS']['id']
    body = module.get_body(environ)
    session = module.get_db_session()()
    task_service = module.env.get_service('tasks_task_service')
    task = task_service.update_task(session, task_id, body)
    if task:
        module.emit_event('task_updated', {'task_id': task.id})
        return module.response(start_response, {'task': task.__dict__})
    return module.response(start_response, {'error': 'Task not found'}, '404 Not Found')

def delete_task(environ, start_response, module):
    task_id = environ['ROUTE_PARAMS']['id']
    session = module.get_db_session()()
    task_service = module.env.get_service('tasks_task_service')
    if task_service.delete_task(session, task_id):
        module.emit_event('task_deleted', {'task_id': task_id})
        return module.response(start_response, {'message': 'Task deleted'})
    return module.response(start_response, {'error': 'Task not found'}, '404 Not Found')
