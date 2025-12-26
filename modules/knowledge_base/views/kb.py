def list_articles(environ, start_response, module):
    session = module.get_db_session()()
    kb_service = module.env.get_service('knowledge_base_kb_service')
    articles = kb_service.list_articles(session)
    return module.response(start_response, {'articles': [a.__dict__ for a in articles]})

def create_article(environ, start_response, module):
    body = module.get_body(environ)
    session = module.get_db_session()()
    kb_service = module.env.get_service('knowledge_base_kb_service')
    article = kb_service.create_article(session, body)
    module.emit_event('kb_article_created', {'article_id': article.id})
    return module.response(start_response, {'article': article.__dict__}, '201 Created')

def get_article(environ, start_response, module):
    article_id = environ['ROUTE_PARAMS']['id']
    session = module.get_db_session()()
    kb_service = module.env.get_service('knowledge_base_kb_service')
    article = kb_service.get_article(session, article_id)
    if article:
        return module.response(start_response, {'article': article.__dict__})
    return module.response(start_response, {'error': 'Article not found'}, '404 Not Found')

def update_article(environ, start_response, module):
    article_id = environ['ROUTE_PARAMS']['id']
    body = module.get_body(environ)
    session = module.get_db_session()()
    kb_service = module.env.get_service('knowledge_base_kb_service')
    article = kb_service.update_article(session, article_id, body)
    if article:
        return module.response(start_response, {'article': article.__dict__})
    return module.response(start_response, {'error': 'Article not found'}, '404 Not Found')

def create_category(environ, start_response, module):
    body = module.get_body(environ)
    session = module.get_db_session()()
    kb_service = module.env.get_service('knowledge_base_kb_service')
    category = kb_service.create_category(session, body)
    return module.response(start_response, {'category': category.__dict__}, '201 Created')
