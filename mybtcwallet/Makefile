install-dep:
	. /venv/bin/activate && pip install -r requirements.txt

celery-worker:
	. /venv/bin/activate && celery -A app.celery worker --loglevel=info --queues=sync_queue

celery-beat:
	. /venv/bin/activate && celery -A app.celery beat --loglevel=info

run-app:
	. /venv/bin/activate && FLASK_DEBUG=1 FLASK_ENV=development FLASK_APP=app.py flask run


