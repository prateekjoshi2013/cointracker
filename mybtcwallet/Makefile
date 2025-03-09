run:
	docker compose up --build -d
stop:
	docker compose down

install-dep:
	. /venv/bin/activate && pip install -r requirements.txt

celery-worker:
	. /venv/bin/activate && APP_MODE=celery celery -A app.celery worker --loglevel=info --queues=sync_queue

celery-beat:
	. /venv/bin/activate && APP_MODE=celery celery -A app.celery beat --loglevel=info

run-app:
	. /venv/bin/activate && APP_MODE=flask-app FLASK_RUN_PORT=8000 FLASK_DEBUG=1 FLASK_ENV=development FLASK_APP=app.py flask run


