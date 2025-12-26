routes = [
    ('/api/kb/articles', 'GET', 'modules.knowledge_base.views.kb.list_articles'),
    ('/api/kb/articles', 'POST', 'modules.knowledge_base.views.kb.create_article'),
    ('/api/kb/articles/<id>', 'GET', 'modules.knowledge_base.views.kb.get_article'),
    ('/api/kb/articles/<id>', 'PUT', 'modules.knowledge_base.views.kb.update_article'),
    ('/api/kb/categories', 'POST', 'modules.knowledge_base.views.kb.create_category'),
]
