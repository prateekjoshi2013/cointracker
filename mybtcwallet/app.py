from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
from sqlalchemy.dialects.mysql import BIGINT

app = Flask(__name__)

# Configuring the app to connect to MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://prateek:root@mysqldb/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

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

class Transaction(db.Model):
    __tablename__ = 'tx'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    address_id = db.Column(db.String(36), db.ForeignKey('addresses.id'), nullable=False)
    from_addresses = db.Column(db.JSON, nullable=False)  # Array of strings (from addresses)
    to_addresses = db.Column(db.JSON, nullable=False)  # Array of strings (to addresses)
    tx_seq = db.Column(BIGINT, nullable=False)  # Transaction sequence number
    timestamp = db.Column(db.Integer, nullable=False)  # Epoch timestamp

    # Relationship with the Address model
    address = db.relationship('Address', backref=db.backref('transactions', lazy=True))

# Create tables in the database (if they don't already exist)
with app.app_context():
    db.create_all()
    seed_data()

@app.route('/')
def index():
    return "Flask App with SQLAlchemy and MySQL!"

if __name__ == '__main__':
    app.run(debug=True)
