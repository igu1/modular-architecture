routes = [
    ('/crm/companies', 'GET', 'modules.crm.views.companies.list_companies'),
    ('/crm/companies', 'POST', 'modules.crm.views.companies.create_company'),
    ('/crm/companies/<id>', 'GET', 'modules.crm.views.companies.get_company'),
    ('/crm/companies/<id>', 'PUT', 'modules.crm.views.companies.update_company'),
    ('/crm/companies/<id>', 'DELETE', 'modules.crm.views.companies.delete_company'),
]
