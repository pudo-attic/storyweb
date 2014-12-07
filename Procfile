web: gunicorn --preload --log-file - tmi.manage:app
worker: celery -A tmi.queue worker
