def list_workflows(environ, start_response, module):
    session = module.get_db_session()()
    workflow_service = module.env.get_service('workflows_workflow_service')
    workflows = workflow_service.list_workflows(session)
    return module.response(start_response, {'workflows': [w.__dict__ for w in workflows]})

def create_workflow(environ, start_response, module):
    body = module.get_body(environ)
    session = module.get_db_session()()
    workflow_service = module.env.get_service('workflows_workflow_service')
    workflow = workflow_service.create_workflow(session, body)
    return module.response(start_response, {'workflow': workflow.__dict__}, '201 Created')

def get_workflow(environ, start_response, module):
    workflow_id = environ['ROUTE_PARAMS']['id']
    session = module.get_db_session()()
    workflow_service = module.env.get_service('workflows_workflow_service')
    workflow = workflow_service.get_workflow(session, workflow_id)
    if workflow:
        return module.response(start_response, {'workflow': workflow.__dict__})
    return module.response(start_response, {'error': 'Workflow not found'}, '404 Not Found')

def add_action(environ, start_response, module):
    workflow_id = environ['ROUTE_PARAMS']['id']
    body = module.get_body(environ)
    body['workflow_id'] = workflow_id
    session = module.get_db_session()()
    workflow_service = module.env.get_service('workflows_workflow_service')
    action = workflow_service.add_action(session, body)
    return module.response(start_response, {'action': action.__dict__}, '201 Created')
