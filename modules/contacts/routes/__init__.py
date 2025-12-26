routes = [
    ('/api/contacts', 'GET', 'modules.contacts.views.contacts.list_contacts'),
    ('/api/contacts', 'POST', 'modules.contacts.views.contacts.create_contact'),
    ('/api/contacts/<id>', 'GET', 'modules.contacts.views.contacts.get_contact'),
    ('/api/contacts/<id>', 'PUT', 'modules.contacts.views.contacts.update_contact'),
    ('/api/contacts/<id>', 'DELETE', 'modules.contacts.views.contacts.delete_contact'),
]
