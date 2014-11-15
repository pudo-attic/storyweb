from flask.ext.script import Manager
from flask.ext.assets import ManageAssets

from storyweb.core import assets
from storyweb.web import app
from storyweb.admin import admin # noqa
from storyweb.model import initdb as initdb_
from storyweb.loader import load as load_


manager = Manager(app)
manager.add_command("assets", ManageAssets(assets))


@manager.command
def initdb():
    """ Destroy the current database and create a new one. """
    initdb_()


@manager.command
def load(filename):
    """ Load blocks from the given file. """
    load_(filename)


@manager.command
def demo():
    from storyweb.model import Block, db
    blocks = db.session.query(Block)
    blocks = blocks.order_by(Block.date.desc()).limit(10)
    for block in blocks:
        html, refs = block.parse()
        print [html, refs]



if __name__ == "__main__":
    manager.run()
