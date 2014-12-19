import logging

from storyweb.core import celery as app
from storyweb.analysis.extract import extract_entities
from storyweb.model import Card, db
from storyweb.search import index_card
from storyweb import spiders

log = logging.getLogger(__name__)


@app.task
def extract(card_id):
    parent = Card.by_id(card_id)
    log.info('Extracting entities from "%s"...', parent.title)
    try:
        extract_entities(parent)
        db.session.commit()
    except Exception, e:
        log.exception(e)


def lookup_all(card_id):
    for spider_name in spiders.SPIDERS:
        lookup.delay(card_id, spider_name)


@app.task
def lookup(card_id, spider_name):
    try:
        card = Card.by_id(card_id)
        spiders.lookup(card, spider_name)
        db.session.commit()
    except Exception, e:
        log.exception(e)


@app.task
def index(card_id):
    try:
        card = Card.by_id(card_id)
        if card is not None:
            index_card(card)
    except Exception, e:
        log.exception(e)
