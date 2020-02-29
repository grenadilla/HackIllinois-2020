from app import db, login

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    #email = db.Column(db.String(120), index=True, unique=True)
    customer_id = db.Column(db.String(24), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    accounts = db.relationship('Account', backref='user')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Account(db.Model):
    __tablename__ = 'accounts'
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.String(24), index=True, unique=True)
    nickname = db.Column(db.String())
    rewards = db.Column(db.Integer)
    balance = db.Column(db.Integer)
    account_number = db.Column(db.String(24))
    user_id = db.Column(db.String(24), db.ForeignKey('users.id'))
    account_type_id = db.Column(db.String(24), db.ForeignKey('account_types.id'))

    def __repr__(self):
        return '<{}>'.format(self.nickname)
    
class AccountType(db.Model):
    __tablename__ = 'account_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24), unique=True)
    accounts = db.relationship('Account', backref='account_type')

    def __repr__(self):
        return '<{} Account>'.format(self.name)
