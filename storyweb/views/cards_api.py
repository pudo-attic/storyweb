from werkzeug.exceptions import Gone
from flask import Blueprint, g, request
from restpager import Pager

from storyweb import authz
from storyweb.model import db, Card
from storyweb.search import search_cards, cards_query
from storyweb.util import jsonify, obj_or_404, request_data
from storyweb.queue import extract


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
    cards = cards.order_by(Card.created_at.desc())
    
    pager = Pager(cards)
    return jsonify(pager, index=True)


@blueprint.route('/api/1/cards/_suggest', methods=['GET'])
def suggest():
    authz.require(authz.logged_in())
    options = Card.suggest(request.args.get('prefix'),
                           categories=request.args.getlist('category'))
    return jsonify({'options': options}, index=True)


@blueprint.route('/api/1/cards/_search', methods=['GET'])
def search():
    authz.require(authz.logged_in())
    query = cards_query(request.args)
    pager = Pager(search_cards(query))
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
