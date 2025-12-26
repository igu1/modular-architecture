routes = [
    ('/api/workflows', 'GET', 'modules.workflows.views.workflows.list_workflows'),
    ('/api/workflows', 'POST', 'modules.workflows.views.workflows.create_workflow'),
    ('/api/workflows/<id>', 'GET', 'modules.workflows.views.workflows.get_workflow'),
    ('/api/workflows/<id>/actions', 'POST', 'modules.workflows.views.workflows.add_action'),
]
