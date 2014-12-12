import logging
from storyweb.core import db
from storyweb.model.user import User
from storyweb.model.card import Card # noqa
from storyweb.model.link import Link # noqa
from storyweb.model.reference import Reference # noqa
from storyweb.model.spider_tag import SpiderTag # noqa

log = logging.getLogger(__name__)


def init_db():
    log.info("Creating database tables...")
    #db.drop_all()
    db.create_all()
    User.default_user()
    db.session.commit()
