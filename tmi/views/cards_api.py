from werkzeug.exceptions import Gone
from flask import Blueprint, g, request
from restpager import Pager

from tmi import authz
from tmi.model import db, Card
from tmi.util import jsonify, obj_or_404, request_data
from tmi.queue import extract


blueprint = Blueprint('cards_api', __name__)


@blueprint.route('/api/1/categories', methods=['GET'])
def categories():
    authz.require(authz.logged_in())
    return jsonify({'categories': Card.CATEGORIES}, index=True)


@blueprint.route('/api/1/cards', methods=['GET'])
def index():
    authz.require(authz.logged_in())
    cards = db.session.query(Card)
    if 'category' in request.args:
        cards = cards.filter(Card.category == request.args.get('category'))
    
    # TODO: find a better solution
    cards = cards.filter(Card.title != '')
    
    pager = Pager(cards)
    return jsonify(pager, index=True)


@blueprint.route('/api/1/cards', methods=['POST', 'PUT'])
def create():
    authz.require(authz.logged_in())
    card = Card().save(request_data(), g.user)
    db.session.commit()
    extract.delay(card.id)
    return jsonify(card, status=201)


@blueprint.route('/api/1/cards/<id>', methods=['GET'])
def view(id):
    authz.require(authz.logged_in())
    card = obj_or_404(Card.by_id(id))
    return jsonify(card)


@blueprint.route('/api/1/cards/<id>', methods=['POST', 'PUT'])
def update(id):
    authz.require(authz.logged_in())
    card = obj_or_404(Card.by_id(id))
    card.save(request_data(), g.user)
    db.session.commit()
    extract.delay(card.id)
    return jsonify(card)


@blueprint.route('/api/1/cards/<id>', methods=['DELETE'])
def delete(id):
    authz.require(authz.logged_in())
    card = obj_or_404(Card.by_id(id))
    db.session.delete(card)
    db.session.commit()
    raise Gone()
