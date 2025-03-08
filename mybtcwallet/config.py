import os

CELERY_BROKER_URL = 'redis://myredis:6379/0'  # Redis as the broker
CELERY_RESULT_BACKEND = 'redis://myredis:6379/0'
DB_USER = os.getenv("MYSQL_USER", "prateek")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD", "root")
DB_HOST = os.getenv("MYSQL_HOST", "mysqldb")
DB_NAME = os.getenv("MYSQL_DATABASE", "mydb")

SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
