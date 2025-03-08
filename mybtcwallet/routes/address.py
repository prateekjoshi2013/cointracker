from flask import Blueprint, jsonify, request
from models import Address


# Create a Blueprint
address_bp = Blueprint("address", __name__)

# GET endpoint to list all addresses
@address_bp.route("/address", methods=["GET"])
def get_addresses():
    addresses = Address.query.all()  # Fetch all addresses from the database
    return jsonify([address.to_dict() for address in addresses])


# POST endpoint to create a new address
@address_bp.route("/address", methods=["POST"])
def create_address():
    try:
        data = request.get_json()  # Parse the incoming JSON data
        # Simple validation of the required fields
        if not all(key in data for key in ["address", "wallet_id"]):
            return jsonify({"error": "Missing one or more required fields"}), 400
        print(data)
        # Create a new address instance
        new_address = Address(
            address=data["address"],
            wallet_id=data["wallet_id"],
        )

        new_address.save()
    except Exception as e:
        print(e)
    return jsonify({"message": "Address created successfully", "address": new_address.to_dict()}), 201