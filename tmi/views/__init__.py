from flask import g
from flask.ext.login import current_user

from tmi.core import app
from tmi.assets import assets # noqa
from tmi.views.ui import ui # noqa
from tmi.views.auth import login, logout # noqa
from tmi.views.admin import admin # noqa
from tmi.views.cards_api import blueprint as cards_api


@app.before_request
def before_request():
    g.user = current_user

app.register_blueprint(cards_api)
