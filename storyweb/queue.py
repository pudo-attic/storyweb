import logging

from storyweb.core import celery as app
from storyweb.model.extract import extract_entities
from storyweb.model import Card, Link, db
from storyweb.search import index_card
from storyweb import spiders

log = logging.getLogger(__name__)


@app.task
def extract(card_id):
    parent = Card.by_id(card_id)
    if parent.category != Card.ARTICLE:
        log.info('Not extracting entities from "%s"...', parent.title)
        return
    log.info('Extracting entities from "%s"...', parent.title)
    try:
        for offset, child in extract_entities(parent.text):
            data = {
                'offset': offset,
                'child': child
            }
            link = Link.find(parent, child)
            if link is None:
                link = Link()
            else:
                data['status'] = link.status
            link.save(data, parent, child.author)
        index.delay(card_id)
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
        index_card(card)
    except Exception, e:
        log.exception(e)
