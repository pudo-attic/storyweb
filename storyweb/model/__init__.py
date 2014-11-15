from storyweb.core import db
from storyweb.model.user import User
from storyweb.model.block import Block # noqa


def initdb():
    db.drop_all()
    db.create_all()
    User.default_user()
    db.session.commit()

