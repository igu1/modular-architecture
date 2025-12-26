class TicketService:
    
    def __init__(self):
        self.name = "ticket_service"
    
    def create_ticket(self, session, ticket_data):
        from modules.tickets.models import Ticket
        ticket = Ticket(**ticket_data)
        session.add(ticket)
        session.commit()
        return ticket
    
    def get_ticket(self, session, ticket_id):
        from modules.tickets.models import Ticket
        return session.query(Ticket).filter(Ticket.id == ticket_id).first()
    
    def update_ticket(self, session, ticket_id, ticket_data):
        from modules.tickets.models import Ticket
        ticket = session.query(Ticket).filter(Ticket.id == ticket_id).first()
        if ticket:
            for key, value in ticket_data.items():
                setattr(ticket, key, value)
            session.commit()
        return ticket
    
    def delete_ticket(self, session, ticket_id):
        from modules.tickets.models import Ticket
        ticket = session.query(Ticket).filter(Ticket.id == ticket_id).first()
        if ticket:
            session.delete(ticket)
            session.commit()
            return True
        return False
    
    def list_tickets(self, session, filters=None):
        from modules.tickets.models import Ticket
        query = session.query(Ticket)
        if filters:
            for key, value in filters.items():
                query = query.filter(getattr(Ticket, key) == value)
        return query.all()
    
    def add_comment(self, session, comment_data):
        from modules.tickets.models import TicketComment
        comment = TicketComment(**comment_data)
        session.add(comment)
        session.commit()
        return comment
