import logging

from storyweb.core import celery as app
from storyweb.analysis.extract import extract_entities
from storyweb.model import Card, db
from storyweb.search import index_card
from storyweb import spiders

log = logging.getLogger(__name__)


@app.task(bind=True)
def extract(self, card_id):
    parent = Card.by_id(card_id)
    if parent is None:
        raise self.retry(countdown=1)
    log.info('Extracting entities from "%s"...', parent.title)
    try:
        extract_entities(parent)
        db.session.commit()
    except Exception, e:
        log.exception(e)
    finally:
        db.session.remove()


def lookup_all(card_id):
    for spider_name in spiders.SPIDERS:
        lookup.apply_async((card_id, spider_name), {}, countdown=1)


@app.task(bind=True)
def lookup(self, card_id, spider_name):
    try:
        card = Card.by_id(card_id)
        if card is None:
            raise self.retry(countdown=1)
        spiders.lookup(card, spider_name)
        db.session.commit()
    except Exception, e:
        log.exception(e)
    finally:
        db.session.remove()


@app.task(bind=True)
def index(self, card_id):
    try:
        card = Card.by_id(card_id)
        if card is None:
            raise self.retry(countdown=2)
        index_card(card)
    except Exception, e:
        log.exception(e)
    finally:
        db.session.remove()
