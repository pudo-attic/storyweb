from flask.ext.script import Manager
from flask.ext.assets import ManageAssets

from storyweb.core import assets
from storyweb.web import app


manager = Manager(app)
manager.add_command("assets", ManageAssets(assets))

if __name__ == "__main__":
    manager.run()
