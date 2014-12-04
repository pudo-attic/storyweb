import logging
from flask.ext.script import Manager
from flask.ext.assets import ManageAssets

from storyweb.core import assets
from storyweb.web import app
from storyweb.admin import admin # noqa
from storyweb.model import initdb as initdb_
from storyweb.loader import load as load_
from storyweb.model import Block, db
from storyweb.model.search import index_block, search_block
from storyweb.model.search import init_elasticsearch


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
    """ (Re-)Index all existing blocks. """
    blocks = db.session.query(Block)
    blocks = blocks.order_by(Block.date.desc())
    for block in blocks.yield_per(500):
        log.info("Indexing %s", block.id)
        index_block(block)


@manager.command
def search(term):
    q = {
        "query": {
            "query_string": {
                "query": term
            }
        }
    }

    for res in search_block(q):
        print res


@manager.command
def demo():
    from storyweb.model import Block, db
    blocks = db.session.query(Block)
    blocks = blocks.order_by(Block.date.desc()).limit(10)
    for block in blocks:
        print block
        

if __name__ == "__main__":
    manager.run()
