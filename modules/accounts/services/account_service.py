class AccountService:
    
    def __init__(self):
        self.name = "account_service"
    
    def create_account(self, session, account_data):
        from modules.accounts.models import Account
        account = Account(**account_data)
        session.add(account)
        session.commit()
        return account
    
    def get_account(self, session, account_id):
        from modules.accounts.models import Account
        return session.query(Account).filter(Account.id == account_id).first()
    
    def update_account(self, session, account_id, account_data):
        from modules.accounts.models import Account
        account = session.query(Account).filter(Account.id == account_id).first()
        if account:
            for key, value in account_data.items():
                setattr(account, key, value)
            session.commit()
        return account
    
    def delete_account(self, session, account_id):
        from modules.accounts.models import Account
        account = session.query(Account).filter(Account.id == account_id).first()
        if account:
            session.delete(account)
            session.commit()
            return True
        return False
    
    def list_accounts(self, session, filters=None):
        from modules.accounts.models import Account
        query = session.query(Account)
        if filters:
            for key, value in filters.items():
                query = query.filter(getattr(Account, key) == value)
        return query.all()
