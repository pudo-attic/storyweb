import os

DEBUG = True
ASSETS_DEBUG = True
SECRET_KEY = 'banana pancakes'

APP_NAME = 'tmi'

db_uri = 'sqlite:///%s.sqlite3' % APP_NAME
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', db_uri)
ELASTICSEARCH_URL = 'http://localhost:9200'

OPENCORPORATES_TOKEN = os.environ.get('OPENCORPORATES_TOKEN')
CALAIS_KEY = os.environ.get('CALAIS_KEY')

CELERY_ALWAYS_EAGER = True
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TIMEZONE = 'UTC'
CELERY_BROKER_URL = os.environ.get('RABBITMQ_BIGWIG_URL',
                                   'amqp://guest:guest@localhost:5672//')
