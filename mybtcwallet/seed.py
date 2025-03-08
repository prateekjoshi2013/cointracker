from models import db, User, Wallet, Address, Transaction, bcrypt
import uuid
import json
import time

# Function to hash passwords
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def seed_data():
    # Clear tables first (use with caution in production)
    db.session.query(Transaction).delete()
    db.session.query(Address).delete()
    db.session.query(Wallet).delete()
    db.session.query(User).delete()
    db.session.commit()
    # Create a User
    user1 = User(
        id=str(uuid.uuid4()),
        firstname="Alice",
        lastname="Doe",
        email="alice@example.com",
        password=hash_password("password123")
    )


    user2 = User(
        id=str(uuid.uuid4()),
        firstname="John",
        lastname="Doe",
        email="john@example.com",
        password=hash_password("password123")
    )


    db.session.add(user1)
    db.session.commit()

    # Create a Wallet for Alice
    wallet1 = Wallet(
        id=str(uuid.uuid4()),
        user_id=user1.id,
        wallet="btc_wallet_001"
    )

    db.session.add(wallet1)
    db.session.commit()

    # Create an Address for Alice's Wallet
    address1 = Address(
        id=str(uuid.uuid4()),
        wallet_id=wallet1.id,
        address="12xQ9k5ousS8MqNsMBqHKtjAtCuKezm2Ju",  # Example Bitcoin address
        curr_balance=None,
        last_synced_tx=None,
    )

    address2 = Address(
        id=str(uuid.uuid4()),
        wallet_id=wallet1.id,
        address="bc1q0sg9rdst255gtldsmcf8rk0764avqy2h2ksqs5",  # Example Bitcoin address
        curr_balance=None,
        last_synced_tx=None,
    )


    db.session.add(address1)
    db.session.add(address2)
    db.session.commit()

    # Create a Transaction for Alice's Address
    # tx1 = Transaction(
    #     id=str(uuid.uuid4()),
    #     address_id=address1.id,
    #     from_addresses=json.dumps(["3FZbgi29cpjq2GjdwV8eyHuJJnkLtktZc5"]),
    #     to_addresses=json.dumps(["1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"]),
    #     tx_seq=1001,
    #     timestamp=int(time.time())
    # )

    # db.session.add(tx1)
    # db.session.commit()

    print("✅ Seed data inserted successfully!")
