import logging
from tmi.core import db
from tmi.model.user import User
from tmi.model.card import Card # noqa
from tmi.model.link import Link # noqa
from tmi.model.reference import Reference # noqa

log = logging.getLogger(__name__)


def initdb():
    log.info("Dropping and creating database tables...")
    db.drop_all()
    db.create_all()
    User.default_user()
    db.session.commit()
