class InvoiceService:
    
    def __init__(self):
        self.name = "invoice_service"
    
    def create_invoice(self, session, invoice_data):
        from modules.invoices.models import Invoice
        invoice = Invoice(**invoice_data)
        session.add(invoice)
        session.commit()
        return invoice
    
    def get_invoice(self, session, invoice_id):
        from modules.invoices.models import Invoice
        return session.query(Invoice).filter(Invoice.id == invoice_id).first()
    
    def update_invoice(self, session, invoice_id, invoice_data):
        from modules.invoices.models import Invoice
        invoice = session.query(Invoice).filter(Invoice.id == invoice_id).first()
        if invoice:
            for key, value in invoice_data.items():
                setattr(invoice, key, value)
            session.commit()
        return invoice
    
    def delete_invoice(self, session, invoice_id):
        from modules.invoices.models import Invoice
        invoice = session.query(Invoice).filter(Invoice.id == invoice_id).first()
        if invoice:
            session.delete(invoice)
            session.commit()
            return True
        return False
    
    def list_invoices(self, session, filters=None):
        from modules.invoices.models import Invoice
        query = session.query(Invoice)
        if filters:
            for key, value in filters.items():
                query = query.filter(getattr(Invoice, key) == value)
        return query.all()
    
    def add_payment(self, session, payment_data):
        from modules.invoices.models import Payment
        payment = Payment(**payment_data)
        session.add(payment)
        session.commit()
        return payment
