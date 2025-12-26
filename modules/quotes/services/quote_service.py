class QuoteService:
    
    def __init__(self):
        self.name = "quote_service"
    
    def create_quote(self, session, quote_data):
        from modules.quotes.models import Quote
        quote = Quote(**quote_data)
        session.add(quote)
        session.commit()
        return quote
    
    def get_quote(self, session, quote_id):
        from modules.quotes.models import Quote
        return session.query(Quote).filter(Quote.id == quote_id).first()
    
    def update_quote(self, session, quote_id, quote_data):
        from modules.quotes.models import Quote
        quote = session.query(Quote).filter(Quote.id == quote_id).first()
        if quote:
            for key, value in quote_data.items():
                setattr(quote, key, value)
            session.commit()
        return quote
    
    def delete_quote(self, session, quote_id):
        from modules.quotes.models import Quote
        quote = session.query(Quote).filter(Quote.id == quote_id).first()
        if quote:
            session.delete(quote)
            session.commit()
            return True
        return False
    
    def list_quotes(self, session, filters=None):
        from modules.quotes.models import Quote
        query = session.query(Quote)
        if filters:
            for key, value in filters.items():
                query = query.filter(getattr(Quote, key) == value)
        return query.all()
    
    def add_line_item(self, session, line_item_data):
        from modules.quotes.models import QuoteLineItem
        line_item = QuoteLineItem(**line_item_data)
        session.add(line_item)
        session.commit()
        return line_item
