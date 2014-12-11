from os import environ as env

APP_NAME = 'tmi'
APP_TITLE = env.get('APP_TITLE', 'Grano StoryWeb')
APP_DESCRIPTION = env.get('APP_DESCRIPTION', 'You know, an IDE for news!')

DEBUG = env.get('DEBUG', '').lower().strip()
DEBUG = DEBUG in ['no', 'false', '0']
ASSETS_DEBUG = DEBUG
SECRET_KEY = env.get('SECRET_KEY', 'banana pancakes')

db_uri = 'sqlite:///%s.sqlite3' % APP_NAME
SQLALCHEMY_DATABASE_URI = env.get('DATABASE_URL', db_uri)
ELASTICSEARCH_URL = env.get('BONSAI_URL', 'http://localhost:9200')

OPENCORPORATES_KEY = env.get('OPENCORPORATES_KEY')
CALAIS_KEY = env.get('CALAIS_KEY')

CELERY_ALWAYS_EAGER = True
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TIMEZONE = 'UTC'
CELERY_BROKER_URL = env.get('RABBITMQ_BIGWIG_URL',
                            'amqp://guest:guest@localhost:5672//')
