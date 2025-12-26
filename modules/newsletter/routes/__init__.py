routes = [
    ('/newsletter/subscribers', 'GET', 'modules.newsletter.views.newsletter.list_subscribers'),
    ('/newsletter/subscribers', 'POST', 'modules.newsletter.views.newsletter.subscribe'),
    ('/newsletter/subscribers/<id>', 'DELETE', 'modules.newsletter.views.newsletter.unsubscribe'),
    ('/newsletter/campaigns', 'GET', 'modules.newsletter.views.newsletter.list_campaigns'),
    ('/newsletter/campaigns', 'POST', 'modules.newsletter.views.newsletter.create_campaign'),
    ('/newsletter/campaigns/<id>', 'GET', 'modules.newsletter.views.newsletter.get_campaign'),
    ('/newsletter/campaigns/<id>/send', 'POST', 'modules.newsletter.views.newsletter.send_campaign'),
]
