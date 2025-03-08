from flask import Flask
import config
from extensions import db
from sync import make_celery
from routes.address import address_bp  # Import the Blueprint
from seed import seed_data

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS
    app.config["CELERY_CONFIG"] = {
        "broker_url": config.CELERY_BROKER_URL, 
        "result_backend": config.CELERY_RESULT_BACKEND
    }

    db.init_app(app)


    celery = make_celery(app)
    celery.set_default() # to associate the task with flask
    app.register_blueprint(address_bp, url_prefix="/api")

    with app.app_context():
            db.drop_all()
            db.create_all()
            seed_data()
    return app, celery


app,celery=create_app()
app.app_context().push() # needed to have the context in celery task