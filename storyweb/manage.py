import logging
from flask.ext.script import Manager
from flask.ext.assets import ManageAssets
from flask.ext.migrate import MigrateCommand

from storyweb.views import app, assets
from storyweb.upgrade import upgrade as upgrade_


log = logging.getLogger(__name__)
manager = Manager(app)
manager.add_command("assets", ManageAssets(assets))
manager.add_command('db', MigrateCommand)


@manager.command
def upgrade():
    """ Upgrade the database and re-index search. """
    upgrade_()


if __name__ == "__main__":
    manager.run()
