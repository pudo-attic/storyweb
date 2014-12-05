from flask import g, request
from flask.ext.login import current_user
from werkzeug.exceptions import HTTPException

from tmi.core import app
from tmi.forms import Invalid
from tmi.util import jsonify
from tmi.assets import assets # noqa
from tmi.views.ui import ui # noqa
from tmi.views.auth import login, logout # noqa
from tmi.views.admin import admin # noqa
from tmi.views.cards_api import blueprint as cards_api


@app.before_request
def before_request():
    g.user = current_user

app.register_blueprint(cards_api)


@app.errorhandler(401)
@app.errorhandler(403)
@app.errorhandler(404)
@app.errorhandler(410)
@app.errorhandler(500)
def handle_exceptions(exc):
    if isinstance(exc, HTTPException):
        message = exc.get_description(request.environ)
        message = message.replace('<p>', '').replace('</p>', '')
        body = {
            'status': exc.code,
            'name': exc.name,
            'message': message
        }
        headers = exc.get_headers(request.environ)
    else:
        body = {
            'status': 500,
            'name': exc.__class__.__name__,
            'message': unicode(exc)
        }
        headers = {}
    return jsonify(body, status=body.get('status'),
                   headers=headers)


@app.errorhandler(Invalid)
def handle_invalid(exc):
    body = {
        'status': 400,
        'name': 'Invalid Data',
        'message': unicode(exc),
        'errors': exc.asdict()
    }
    return jsonify(body, status=400)
