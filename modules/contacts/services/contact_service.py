class ContactService:
    
    def __init__(self):
        self.name = "contact_service"
    
    def create_contact(self, session, contact_data):
        from modules.contacts.models import Contact
        contact = Contact(**contact_data)
        session.add(contact)
        session.commit()
        return contact
    
    def get_contact(self, session, contact_id):
        from modules.contacts.models import Contact
        return session.query(Contact).filter(Contact.id == contact_id).first()
    
    def update_contact(self, session, contact_id, contact_data):
        from modules.contacts.models import Contact
        contact = session.query(Contact).filter(Contact.id == contact_id).first()
        if contact:
            for key, value in contact_data.items():
                setattr(contact, key, value)
            session.commit()
        return contact
    
    def delete_contact(self, session, contact_id):
        from modules.contacts.models import Contact
        contact = session.query(Contact).filter(Contact.id == contact_id).first()
        if contact:
            session.delete(contact)
            session.commit()
            return True
        return False
    
    def list_contacts(self, session, filters=None):
        from modules.contacts.models import Contact
        query = session.query(Contact)
        if filters:
            for key, value in filters.items():
                query = query.filter(getattr(Contact, key) == value)
        return query.all()
