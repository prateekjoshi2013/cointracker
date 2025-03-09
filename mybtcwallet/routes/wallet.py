from flask import Blueprint, jsonify, request
from models import Wallet
from extensions import db
from client.blockchain import addresses_balance

# Create a Blueprint
wallet_bp = Blueprint("wallet", __name__)

# GET endpoint to list all addresses
@wallet_bp.route("/wallet", methods=["GET"])
def get_addresses():
    wallets = Wallet.query.all()
    wallet_dicts=[wallet.to_dict() for wallet in wallets]
    return jsonify(wallet_dicts)

