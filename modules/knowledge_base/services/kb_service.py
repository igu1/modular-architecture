class KBService:
    
    def __init__(self):
        self.name = "kb_service"
    
    def create_article(self, session, article_data):
        from modules.knowledge_base.models import KBArticle
        article = KBArticle(**article_data)
        session.add(article)
        session.commit()
        return article
    
    def get_article(self, session, article_id):
        from modules.knowledge_base.models import KBArticle
        return session.query(KBArticle).filter(KBArticle.id == article_id).first()
    
    def update_article(self, session, article_id, article_data):
        from modules.knowledge_base.models import KBArticle
        article = session.query(KBArticle).filter(KBArticle.id == article_id).first()
        if article:
            for key, value in article_data.items():
                setattr(article, key, value)
            session.commit()
        return article
    
    def list_articles(self, session, filters=None):
        from modules.knowledge_base.models import KBArticle
        query = session.query(KBArticle)
        if filters:
            for key, value in filters.items():
                query = query.filter(getattr(KBArticle, key) == value)
        return query.all()
    
    def create_category(self, session, category_data):
        from modules.knowledge_base.models import KBCategory
        category = KBCategory(**category_data)
        session.add(category)
        session.commit()
        return category
