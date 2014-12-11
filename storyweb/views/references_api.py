from werkzeug.exceptions import Gone
from flask import Blueprint, g
from restpager import Pager

from storyweb import authz
from storyweb.model import db, Card, Reference
from storyweb.util import jsonify, obj_or_404, request_data


blueprint = Blueprint('references_api', __name__)


@blueprint.route('/api/1/cards/<card_id>/references', methods=['GET'])
def index(card_id):
    authz.require(authz.logged_in())
    card = obj_or_404(Card.by_id(card_id))
    references = db.session.query(Reference)
    references = references.filter(Reference.card == card)
    pager = Pager(references, card_id=card_id)
    return jsonify(pager, index=True)


@blueprint.route('/api/1/cards/<card_id>/references', methods=['POST', 'PUT'])
def create(card_id):
    authz.require(authz.logged_in())
    card = obj_or_404(Card.by_id(card_id))
    reference = Reference().save(request_data(), card, g.user)
    db.session.commit()
    return jsonify(reference, status=201)


@blueprint.route('/api/1/cards/<card_id>/references/<id>', methods=['GET'])
def view(card_id, id):
    authz.require(authz.logged_in())
    reference = obj_or_404(Reference.by_id(id, card_id=card_id))
    return jsonify(reference)


@blueprint.route('/api/1/cards/<card_id>/references/<id>', methods=['POST', 'PUT'])
def update(card_id, id):
    authz.require(authz.logged_in())
    reference = obj_or_404(Reference.by_id(id, card_id=card_id))
    reference.save(request_data(), reference.card, g.user)
    db.session.commit()
    return jsonify(reference)


@blueprint.route('/api/1/cards/<card_id>/references/<id>', methods=['DELETE'])
def delete(card_id, id):
    authz.require(authz.logged_in())
    reference = obj_or_404(Reference.by_id(id, card_id=card_id))
    db.session.delete(reference)
    db.session.commit()
    raise Gone()
