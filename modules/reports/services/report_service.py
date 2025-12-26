class ReportService:
    
    def __init__(self):
        self.name = "report_service"
    
    def create_report(self, session, report_data):
        from modules.reports.models import Report
        report = Report(**report_data)
        session.add(report)
        session.commit()
        return report
    
    def get_report(self, session, report_id):
        from modules.reports.models import Report
        return session.query(Report).filter(Report.id == report_id).first()
    
    def list_reports(self, session, filters=None):
        from modules.reports.models import Report
        query = session.query(Report)
        if filters:
            for key, value in filters.items():
                query = query.filter(getattr(Report, key) == value)
        return query.all()
    
    def schedule_report(self, session, schedule_data):
        from modules.reports.models import ReportSchedule
        schedule = ReportSchedule(**schedule_data)
        session.add(schedule)
        session.commit()
        return schedule
