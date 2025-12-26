routes = [
    ('/api/campaigns', 'GET', 'modules.campaigns.views.campaigns.list_campaigns'),
    ('/api/campaigns', 'POST', 'modules.campaigns.views.campaigns.create_campaign'),
    ('/api/campaigns/<id>', 'GET', 'modules.campaigns.views.campaigns.get_campaign'),
    ('/api/campaigns/<id>', 'PUT', 'modules.campaigns.views.campaigns.update_campaign'),
    ('/api/campaigns/<id>', 'DELETE', 'modules.campaigns.views.campaigns.delete_campaign'),
    ('/api/campaigns/<id>/members', 'POST', 'modules.campaigns.views.campaigns.add_member'),
]
