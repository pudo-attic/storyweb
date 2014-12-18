import logging
from flask import Flask
from flask import url_for as _url_for
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.assets import Environment
from flask.ext.migrate import Migrate
from kombu import Exchange, Queue
from celery import Celery
from pyelasticsearch import ElasticSearch

from storyweb import default_settings

logging.basicConfig(level=logging.DEBUG)

# specific loggers
logging.getLogger('requests').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)
logging.getLogger('pyelasticsearch').setLevel(logging.WARNING)


app = Flask(__name__)
app.config.from_object(default_settings)
app.config.from_envvar('STORYWEB_SETTINGS', silent=True)
app_name = app.config.get('APP_NAME')

db = SQLAlchemy(app)
migrate = Migrate(app, db, directory=app.config.get('ALEMBIC_DIR'))

es = ElasticSearch(app.config.get('ELASTICSEARCH_URL'))
es_index = app.config.get('ELASTICSEARCH_INDEX', app_name)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

queue_name = app_name + '_q'
app.config['CELERY_DEFAULT_QUEUE'] = queue_name
app.config['CELERY_QUEUES'] = (
    Queue(queue_name, Exchange(queue_name), routing_key=queue_name),
)

celery = Celery(app_name, broker=app.config['CELERY_BROKER_URL'])
celery.config_from_object(app.config)

assets = Environment(app)


def url_for(*a, **kw):
    try:
        kw['_external'] = True
        return _url_for(*a, **kw)
    except RuntimeError:
        return None
