def list_templates(environ, start_response, module):
    session = module.get_db_session()()
    service = module.env.get_service('email_marketing_email_marketing_service')
    templates = service.list_templates(session)
    return module.response(start_response, {'templates': [t.__dict__ for t in templates]})

def create_template(environ, start_response, module):
    body = module.get_body(environ)
    session = module.get_db_session()()
    service = module.env.get_service('email_marketing_email_marketing_service')
    template = service.create_template(session, body)
    return module.response(start_response, {'template': template.__dict__}, '201 Created')

def list_email_campaigns(environ, start_response, module):
    session = module.get_db_session()()
    service = module.env.get_service('email_marketing_email_marketing_service')
    campaigns = service.list_email_campaigns(session)
    return module.response(start_response, {'campaigns': [c.__dict__ for c in campaigns]})

def create_email_campaign(environ, start_response, module):
    body = module.get_body(environ)
    session = module.get_db_session()()
    service = module.env.get_service('email_marketing_email_marketing_service')
    campaign = service.create_email_campaign(session, body)
    module.emit_event('email_campaign_created', {'campaign_id': campaign.id})
    return module.response(start_response, {'campaign': campaign.__dict__}, '201 Created')
