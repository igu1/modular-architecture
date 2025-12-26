routes = [
    ('/api/email-templates', 'GET', 'modules.email_marketing.views.email_marketing.list_templates'),
    ('/api/email-templates', 'POST', 'modules.email_marketing.views.email_marketing.create_template'),
    ('/api/email-campaigns', 'GET', 'modules.email_marketing.views.email_marketing.list_email_campaigns'),
    ('/api/email-campaigns', 'POST', 'modules.email_marketing.views.email_marketing.create_email_campaign'),
]
