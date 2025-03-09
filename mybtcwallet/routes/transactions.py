from flask import request, jsonify, Blueprint
from models import Transaction
from extensions import db
from sqlalchemy import text


# Create a Blueprint
transactions_bp = Blueprint("transactions", __name__)

# Helper method to serialize transaction data (you can modify as needed)
def transaction_to_dict(transaction):
    return {
        'id': transaction.id,
        'address_id': transaction.address_id,
        'from_addresses': transaction.from_addresses,
        'to_addresses': transaction.to_addresses,
        'fee': transaction.fee,
        'result': transaction.result,
        'balance': transaction.balance,
        'timestamp': transaction.timestamp,
    }

# Paginated API to get transactions
@transactions_bp.route('/transactions', methods=['GET'])
def get_transactions():
    # Get pagination parameters from request (default: page 1, 10 records per page)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Start a new session with READ COMMITTED isolation level
    session = db.session()
    session.execute(text("SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED"))
    
    # Get paginated transactions
    transactions = (
        session.query(Transaction)
        .order_by(Transaction.timestamp.desc())  # Order by timestamp or any column
        .paginate(page=page, per_page=per_page, error_out=False)  # Pagination logic
    )
    
    # Format response (converting results to a list of dictionaries)
    result = {
        'total': transactions.total,
        'pages': transactions.pages,
        'current_page': transactions.page,
        'per_page': transactions.per_page,
        'transactions': [transaction_to_dict(transaction) for transaction in transactions.items],
    }
    
    # Close session after query
    session.close()
    
    return jsonify(result)



