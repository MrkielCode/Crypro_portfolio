from portfolio import db
from datetime import datetime
from portfolio import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    """ users tables """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    transactions = db.relationship('Transaction', back_populates='user', lazy=True)

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"

class Transaction(db.Model):
    """ Transactions table """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    asset_name = db.Column(db.String(20), nullable=False)
    quantity = db.Column(db.Float, nullable=False, default=0)
    cost = db.Column(db.Float, nullable=False, default=0)
    transaction_type = db.Column(db.Integer, default=1)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    user = db.relationship('User', back_populates='transactions')
    
    def __repr__(self):
        return (
            f"<Transaction(id={self.id}, user_id={self.user_id}, "
            f"asset_name={self.asset_name}, quantity={self.quantity}, "
            f"cost={self.cost}, date={self.date}, "
            f"type={self.transaction_type})>"
            )
