def list_campaigns(environ, start_response, module):
    session = module.get_db_session()()
    campaign_service = module.env.get_service('campaigns_campaign_service')
    campaigns = campaign_service.list_campaigns(session)
    return module.response(start_response, {'campaigns': [c.__dict__ for c in campaigns]})

def create_campaign(environ, start_response, module):
    body = module.get_body(environ)
    session = module.get_db_session()()
    campaign_service = module.env.get_service('campaigns_campaign_service')
    campaign = campaign_service.create_campaign(session, body)
    module.emit_event('campaign_created', {'campaign_id': campaign.id})
    return module.response(start_response, {'campaign': campaign.__dict__}, '201 Created')

def get_campaign(environ, start_response, module):
    campaign_id = environ['ROUTE_PARAMS']['id']
    session = module.get_db_session()()
    campaign_service = module.env.get_service('campaigns_campaign_service')
    campaign = campaign_service.get_campaign(session, campaign_id)
    if campaign:
        return module.response(start_response, {'campaign': campaign.__dict__})
    return module.response(start_response, {'error': 'Campaign not found'}, '404 Not Found')

def update_campaign(environ, start_response, module):
    campaign_id = environ['ROUTE_PARAMS']['id']
    body = module.get_body(environ)
    session = module.get_db_session()()
    campaign_service = module.env.get_service('campaigns_campaign_service')
    campaign = campaign_service.update_campaign(session, campaign_id, body)
    if campaign:
        module.emit_event('campaign_updated', {'campaign_id': campaign.id})
        return module.response(start_response, {'campaign': campaign.__dict__})
    return module.response(start_response, {'error': 'Campaign not found'}, '404 Not Found')

def delete_campaign(environ, start_response, module):
    campaign_id = environ['ROUTE_PARAMS']['id']
    session = module.get_db_session()()
    campaign_service = module.env.get_service('campaigns_campaign_service')
    if campaign_service.delete_campaign(session, campaign_id):
        module.emit_event('campaign_deleted', {'campaign_id': campaign_id})
        return module.response(start_response, {'message': 'Campaign deleted'})
    return module.response(start_response, {'error': 'Campaign not found'}, '404 Not Found')

def add_member(environ, start_response, module):
    campaign_id = environ['ROUTE_PARAMS']['id']
    body = module.get_body(environ)
    body['campaign_id'] = campaign_id
    session = module.get_db_session()()
    campaign_service = module.env.get_service('campaigns_campaign_service')
    member = campaign_service.add_member(session, body)
    return module.response(start_response, {'member': member.__dict__}, '201 Created')
