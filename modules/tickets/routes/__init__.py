routes = [
    ('/api/tickets', 'GET', 'modules.tickets.views.tickets.list_tickets'),
    ('/api/tickets', 'POST', 'modules.tickets.views.tickets.create_ticket'),
    ('/api/tickets/<id>', 'GET', 'modules.tickets.views.tickets.get_ticket'),
    ('/api/tickets/<id>', 'PUT', 'modules.tickets.views.tickets.update_ticket'),
    ('/api/tickets/<id>', 'DELETE', 'modules.tickets.views.tickets.delete_ticket'),
    ('/api/tickets/<id>/comments', 'POST', 'modules.tickets.views.tickets.add_comment'),
]
