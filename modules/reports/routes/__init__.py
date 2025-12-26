routes = [
    ('/api/reports', 'GET', 'modules.reports.views.reports.list_reports'),
    ('/api/reports', 'POST', 'modules.reports.views.reports.create_report'),
    ('/api/reports/<id>', 'GET', 'modules.reports.views.reports.get_report'),
    ('/api/reports/<id>/schedule', 'POST', 'modules.reports.views.reports.schedule_report'),
]
