import logging
from tmi.core import db
from tmi.model.user import User
from tmi.model.block import Block # noqa
from tmi.model.entity import Entity # noqa
from tmi.model.location import Location # noqa

log = logging.getLogger(__name__)


def initdb():
    log.info("Dropping and creating database tables...")
    db.drop_all()
    db.create_all()
    User.default_user()
    db.session.commit()
