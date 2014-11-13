import logging

from flask import Flask
from flask.ext.assets import Environment, Bundle
from flask.ext.sqlalchemy import SQLAlchemy

from storyweb import default_settings

logging.basicConfig(level=logging.DEBUG)


app = Flask(__name__)
app.config.from_object(default_settings)
app.config.from_envvar('STORYWEB_SETTINGS', silent=True)
app_name = app.config.get('APP_NAME')

db = SQLAlchemy(app)
assets = Environment(app)

assets.register('css', Bundle('style/app.less',
                              filters='less',
                              output='assets/style.css'))

assets.register('js', Bundle("js/app.js",
                             #filters='uglifyjs',
                             output='assets/app.js'))
