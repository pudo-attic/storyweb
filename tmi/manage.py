import logging
from flask.ext.script import Manager
from flask.ext.assets import ManageAssets

from tmi.core import assets
from tmi.web import app
from tmi.admin import admin # noqa
from tmi.model import initdb as initdb_
from tmi.loader import load as load_
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
def load(filename):
    """ Load blocks from the given file. """
    load_(filename)


@manager.command
def index():
    """ (Re-)Index all existing cards. """
    cards = db.session.query(Card)
    cards = cards.order_by(Card.created_at.desc())
    for card in cards.yield_per(500):
        log.info("Indexing %s", card.id)
        #index_block(block)


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
    from tmi.model import Block, db
    blocks = db.session.query(Block)
    blocks = blocks.order_by(Block.date.desc()).limit(10)
    for block in blocks:
        print block
        

if __name__ == "__main__":
    manager.run()
