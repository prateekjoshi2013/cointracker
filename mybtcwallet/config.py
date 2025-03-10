import os

APP_MODE = os.getenv("APP_MODE")
REDIS_HOST = os.getenv("REDIS_HOST", "myredis")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_DB = os.getenv("REDIS_DB", 0)
DB_USER = os.getenv("MYSQL_USER", "prateek")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD", "root")
DB_HOST = os.getenv("MYSQL_HOST", "mysqldb")
DB_NAME = os.getenv("MYSQL_DATABASE", "mydb")
CELERY_BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}'  # Redis as the broker
CELERY_RESULT_BACKEND = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}'
CELERY_BEAT_INTERVAL =  os.getenv("CELERY_BEAT_INTERVAL", 2)
CELERY_QUEUE = os.getenv("CELERY_QUEUE", "sync_queue")
SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
