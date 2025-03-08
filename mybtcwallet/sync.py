from celery import Celery
from celery.schedules import crontab

def make_celery(app):
    celery = Celery(app.import_name)
    celery.conf.update(app.config["CELERY_CONFIG"])
    celery.conf.update(
        imports=('tasks',)  # Explicitly import tasks
    )
    celery.conf.beat_schedule = {
        "sync-every-5-min": {
            "task": "tasks.sync_tx_data",
            "schedule": crontab(minute="*/2"),  # Run every 5 minutes
            "options": {"queue": "sync_queue"},
        },
    }

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery