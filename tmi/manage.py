import logging
from flask.ext.script import Manager
from flask.ext.assets import ManageAssets

from tmi.core import assets
from tmi.web import app
from tmi.admin import admin # noqa
from tmi.model import initdb as initdb_
from tmi.model import Card, db
from tmi.model.search import index_card, search_cards
from tmi.model.search import init_elasticsearch


log = logging.getLogger(__name__)
manager = Manager(app)
manager.add_command("assets", ManageAssets(assets))


@manager.command
def initdb():
    """ Destroy the current database and create a new one. """
    initdb_()
    init_elasticsearch()


@manager.command
def index():
    """ (Re-)Index all existing cards. """
    cards = db.session.query(Card)
    cards = cards.order_by(Card.created_at.desc())
    for card in cards.yield_per(500):
        log.info("Indexing %s", card.id)
        index_card(card)


@manager.command
def search(term):
    q = {
        "query": {
            "query_string": {
                "query": term
            }
        }
    }

    for res in search_cards(q):
        print res


@manager.command
def demo():
    from tmi.model import Card, db
    cards = db.session.query(Card)
    cards = cards.order_by(Card.created_at.desc()).limit(10)
    for card in cards:
        print card
        

if __name__ == "__main__":
    manager.run()
