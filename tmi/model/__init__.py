import logging
from storyweb.core import db
from storyweb.model.user import User
from storyweb.model.block import Block # noqa
from storyweb.model.entity import Entity # noqa
from storyweb.model.location import Location # noqa

log = logging.getLogger(__name__)


def initdb():
    log.info("Dropping and creating database tables...")
    db.drop_all()
    db.create_all()
    User.default_user()
    db.session.commit()
