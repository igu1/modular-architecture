def list_opportunities(environ, start_response, module):
    session = module.get_db_session()()
    opportunity_service = module.env.get_service('opportunities_opportunity_service')
    opportunities = opportunity_service.list_opportunities(session)
    return module.response(start_response, {'opportunities': [o.__dict__ for o in opportunities]})

def create_opportunity(environ, start_response, module):
    body = module.get_body(environ)
    session = module.get_db_session()()
    opportunity_service = module.env.get_service('opportunities_opportunity_service')
    opportunity = opportunity_service.create_opportunity(session, body)
    module.emit_event('opportunity_created', {'opportunity_id': opportunity.id})
    return module.response(start_response, {'opportunity': opportunity.__dict__}, '201 Created')

def get_opportunity(environ, start_response, module):
    opportunity_id = environ['ROUTE_PARAMS']['id']
    session = module.get_db_session()()
    opportunity_service = module.env.get_service('opportunities_opportunity_service')
    opportunity = opportunity_service.get_opportunity(session, opportunity_id)
    if opportunity:
        return module.response(start_response, {'opportunity': opportunity.__dict__})
    return module.response(start_response, {'error': 'Opportunity not found'}, '404 Not Found')

def update_opportunity(environ, start_response, module):
    opportunity_id = environ['ROUTE_PARAMS']['id']
    body = module.get_body(environ)
    session = module.get_db_session()()
    opportunity_service = module.env.get_service('opportunities_opportunity_service')
    opportunity = opportunity_service.update_opportunity(session, opportunity_id, body)
    if opportunity:
        module.emit_event('opportunity_updated', {'opportunity_id': opportunity.id})
        return module.response(start_response, {'opportunity': opportunity.__dict__})
    return module.response(start_response, {'error': 'Opportunity not found'}, '404 Not Found')

def delete_opportunity(environ, start_response, module):
    opportunity_id = environ['ROUTE_PARAMS']['id']
    session = module.get_db_session()()
    opportunity_service = module.env.get_service('opportunities_opportunity_service')
    if opportunity_service.delete_opportunity(session, opportunity_id):
        module.emit_event('opportunity_deleted', {'opportunity_id': opportunity_id})
        return module.response(start_response, {'message': 'Opportunity deleted'})
    return module.response(start_response, {'error': 'Opportunity not found'}, '404 Not Found')

def get_pipeline(environ, start_response, module):
    params = module.get_params(environ)
    user_id = params.get('user_id')
    session = module.get_db_session()()
    opportunity_service = module.env.get_service('opportunities_opportunity_service')
    pipeline = opportunity_service.get_pipeline(session, user_id)
    return module.response(start_response, {'pipeline': [o.__dict__ for o in pipeline]})
