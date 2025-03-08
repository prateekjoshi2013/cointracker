from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
from sqlalchemy.dialects.mysql import BIGINT
import config
from seed import seed_data
from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS

db.init_app(app)

@app.route('/')
def index():
    return "Flask App with SQLAlchemy and MySQL!"

if __name__ == '__main__':
    from seed import seed_data 
    with app.app_context():
        db.create_all()
        seed_data()

    app.run(debug=True, host="0.0.0.0")
