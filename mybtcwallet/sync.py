from celery import Celery
from celery.schedules import crontab
from config import CELERY_BEAT_INTERVAL,CELERY_QUEUE

def make_celery(app):
    celery = Celery(app.import_name)
    celery.conf.update(app.config["CELERY_CONFIG"])
    celery.conf.update(
        imports=('tasks',)  # Explicitly import tasks
    )
    celery.conf.beat_schedule = {
        f"sync-every-{CELERY_BEAT_INTERVAL}-min": {
            "task": "tasks.sync_tx_data",
            "schedule": crontab(minute=f"*/{CELERY_BEAT_INTERVAL}"),  # Run every 2 minutes
            "options": {"queue": f"{CELERY_QUEUE}"},
        },
    }

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery