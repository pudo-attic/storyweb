from os import environ as env, path, getcwd

APP_NAME = 'storyweb'
APP_TITLE = env.get('APP_TITLE', 'StoryWeb')
APP_DESCRIPTION = env.get('APP_DESCRIPTION', 'networked data for news in context')

MOTD = '''
    This is a demo instance. You can log in using the username
    <strong>admin@grano.cc</strong> and the password <strong>admin</strong>.
'''

DEBUG = env.get('DEBUG', '').lower().strip()
DEBUG = DEBUG not in ['no', 'false', '0']
ASSETS_DEBUG = DEBUG
SECRET_KEY = env.get('SECRET_KEY', 'banana pancakes')

ALEMBIC_DIR = path.join(path.dirname(__file__), 'migrate')
ALEMBIC_DIR = path.abspath(ALEMBIC_DIR)

db_uri = 'sqlite:///%s.sqlite3' % path.join(getcwd(), APP_NAME)
SQLALCHEMY_DATABASE_URI = env.get('DATABASE_URL', db_uri)
ELASTICSEARCH_URL = env.get('BONSAI_URL', 'http://localhost:9200')

OPENCORPORATES_KEY = env.get('OPENCORPORATES_KEY')
CALAIS_KEY = env.get('CALAIS_KEY')

CELERY_ALWAYS_EAGER = False
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TIMEZONE = 'UTC'
CELERY_BROKER_URL = env.get('RABBITMQ_BIGWIG_URL',
                            'amqp://guest:guest@localhost:5672//')
