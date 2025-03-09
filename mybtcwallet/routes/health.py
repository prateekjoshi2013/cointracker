from flask import Blueprint, jsonify, request
# Create a Blueprint
health_bp = Blueprint("health", __name__)

# GET endpoint to list all addresses
@health_bp.route("/health", methods=["GET"])
def get_health():
    return jsonify({}), 200

