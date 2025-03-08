from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import BIGINT
import uuid
import bcrypt
import json
import time

db = SQLAlchemy()

def generate_uuid():
    return str(uuid.uuid4())

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

# Models for the database schema
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # Hashed password

class Wallet(db.Model):
    __tablename__ = 'wallet'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    wallet = db.Column(db.String(255), nullable=False)  # Bitcoin wallet ID

    # Relationship with the User model
    user = db.relationship('User', backref=db.backref('wallets', lazy=True))

class Address(db.Model):
    __tablename__ = 'addresses'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    address = db.Column(db.String(255), nullable=False)  # Bitcoin address
    wallet_id = db.Column(db.String(36), db.ForeignKey('wallet.id'), nullable=False)
    curr_balance = db.Column(db.Float, nullable=False)  # Current balance for the Bitcoin address

    # Relationship with the Wallet model
    wallet = db.relationship('Wallet', backref=db.backref('addresses', lazy=True))

    def __repr__(self):
        return f"<Address id: {self.id} addr: {self.address} balance: {self.curr_balance}>"

class Transaction(db.Model):
    __tablename__ = 'tx'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    address_id = db.Column(db.String(36), db.ForeignKey('addresses.id'), nullable=False)
    from_addresses = db.Column(db.JSON, nullable=False)  # List of {address: string, value: float}
    to_addresses = db.Column(db.JSON, nullable=False)  # List of {address: string, value: float}
    tx_seq = db.Column(db.BigInteger, nullable=False)
    fee = db.Column(db.Float, nullable=False)
    result = db.Column(db.Float, nullable=False)
    balance = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.BigInteger, nullable=False)  # Epoch timestamp

    # Relationship with the Address model
    address = db.relationship('Address', backref=db.backref('transactions', lazy=True))

    def __repr__(self):
        return f"<Transaction {self.id} (seq: {self.tx_seq})>"
