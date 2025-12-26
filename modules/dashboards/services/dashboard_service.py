class DashboardService:
    
    def __init__(self):
        self.name = "dashboard_service"
    
    def create_dashboard(self, session, dashboard_data):
        from modules.dashboards.models import Dashboard
        dashboard = Dashboard(**dashboard_data)
        session.add(dashboard)
        session.commit()
        return dashboard
    
    def get_dashboard(self, session, dashboard_id):
        from modules.dashboards.models import Dashboard
        return session.query(Dashboard).filter(Dashboard.id == dashboard_id).first()
    
    def list_dashboards(self, session, filters=None):
        from modules.dashboards.models import Dashboard
        query = session.query(Dashboard)
        if filters:
            for key, value in filters.items():
                query = query.filter(getattr(Dashboard, key) == value)
        return query.all()
    
    def add_widget(self, session, widget_data):
        from modules.dashboards.models import DashboardWidget
        widget = DashboardWidget(**widget_data)
        session.add(widget)
        session.commit()
        return widget
