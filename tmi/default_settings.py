import os

APP_NAME = 'tmi'
PROJECT_NAME = os.environ.get('PROJECT_NAME', 'Grano StoryWeb')
PROJECT_DESCRIPTION = os.environ.get('PROJECT_DESCRIPTION',
                                     'You know, an IDE for news!')

DEBUG = os.environ.get('DEBUG', '').lower().strip()
DEBUG = DEBUG in ['no', 'false', '0']
ASSETS_DEBUG = DEBUG
SECRET_KEY = os.environ.get('SECRET_KEY', 'banana pancakes')

db_uri = 'sqlite:///%s.sqlite3' % APP_NAME
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', db_uri)
ELASTICSEARCH_URL = os.environ.get('BONSAI_URL',
                                   'http://localhost:9200')

OPENCORPORATES_KEY = os.environ.get('OPENCORPORATES_KEY')
CALAIS_KEY = os.environ.get('CALAIS_KEY')

CELERY_ALWAYS_EAGER = True
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TIMEZONE = 'UTC'
CELERY_BROKER_URL = os.environ.get('RABBITMQ_BIGWIG_URL',
                                   'amqp://guest:guest@localhost:5672//')
