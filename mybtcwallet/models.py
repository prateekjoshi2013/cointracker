from extensions import db
from sqlalchemy.dialects.mysql import BIGINT
import uuid
import bcrypt
import json
import time

def generate_uuid():
    return str(uuid.uuid4())

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

# Models for the database schema
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(36), primary_key=True, default=lambda: generate_uuid())
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # Hashed password

class Wallet(db.Model):
    __tablename__ = 'wallet'
    id = db.Column(db.String(36), primary_key=True, default=lambda: generate_uuid())
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    wallet = db.Column(db.String(255), nullable=False)  # Bitcoin wallet ID

    # Relationship with the User model
    user = db.relationship('User', backref=db.backref('wallets', lazy=True))

class Address(db.Model):
    __tablename__ = 'addresses'
    id = db.Column(db.String(36), primary_key=True, default=lambda: generate_uuid())
    address = db.Column(db.String(255), nullable=False, unique=True)  # Bitcoin address
    wallet_id = db.Column(db.String(36), db.ForeignKey('wallet.id'), nullable=False)
    curr_balance = db.Column(db.Float, default=None, nullable=True)  # Current balance for the Bitcoin address
    last_synced_tx = db.Column(db.BigInteger, nullable=True)
    # Relationship with the Wallet model
    wallet = db.relationship('Wallet', backref=db.backref('addresses', lazy=True))

    
     # Add the to_dict() method to convert model instance to a dictionary
    def to_dict(self):
        return {
            "id": self.id,
            "address": self.address,
            "wallet_id": self.wallet_id,
            "curr_balance": self.curr_balance,
            "last_synced_tx": self.last_synced_tx,
        }

    def __repr__(self):
        return f"<Address id: {self.id} addr: {self.address} balance: {self.curr_balance}>"

class Transaction(db.Model):
    __tablename__ = 'tx'
    id = db.Column(db.String(36), primary_key=True, default=lambda: generate_uuid())
    address_id = db.Column(db.String(36), db.ForeignKey('addresses.id'), nullable=False)
    from_addresses = db.Column(db.JSON, nullable=False)  # List of {address: string, value: float}
    to_addresses = db.Column(db.JSON, nullable=False)  # List of {address: string, value: float}
    fee = db.Column(db.Float, nullable=False)
    result = db.Column(db.Float, nullable=False)
    balance = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.BigInteger, nullable=False)  # Epoch timestamp
    txid = db.Column(db.String(64), unique=True, nullable=False)  # Add this line to store txid


    # Relationship with the Address model
    address = db.relationship('Address', backref=db.backref('transactions', lazy=True))

    def __repr__(self):
        return f"<Transaction {self.id} (seq: {self.tx_seq})>"
