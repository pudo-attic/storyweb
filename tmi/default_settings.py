import os

DEBUG = True
ASSETS_DEBUG = True
SECRET_KEY = 'banana pancakes'


APP_NAME = 'tmi'

db_uri = 'sqlite:///%s.sqlite3' % APP_NAME
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', db_uri)

WTF_CSRF_ENABLED = False

ELASTICSEARCH_URL = 'http://localhost:9200'
