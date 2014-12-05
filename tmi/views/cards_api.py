from werkzeug.exceptions import Gone
from flask import Blueprint, request
from restpager import Pager

from tmi.model import db, Card
from tmi.util import jsonify, obj_or_404, request_data


blueprint = Blueprint('cards_api', __name__)


@blueprint.route('/api/1/categories', methods=['GET'])
def categories():
    return jsonify({'categories': Card.CATEGORIES}, index=True)


@blueprint.route('/api/1/cards', methods=['GET'])
def index():
    cards = db.session.query(Card)
    pager = Pager(cards)
    return jsonify(pager, index=True)


@blueprint.route('/api/1/cards', methods=['POST', 'PUT'])
def create():
    return jsonify({}, status=201)


@blueprint.route('/api/1/cards/<id>', methods=['GET'])
def view(id):
    card = obj_or_404(Card.by_id(id))
    return jsonify(card)


@blueprint.route('/api/1/cards/<id>', methods=['POST', 'PUT'])
def update(id):
    card = obj_or_404(Card.by_id(id))
    return jsonify(card)


@blueprint.route('/api/1/cards/<id>', methods=['DELETE'])
def delete(id):
    card = obj_or_404(Card.by_id(id))
    raise Gone()
