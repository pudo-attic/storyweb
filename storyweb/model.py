from storyweb.core import db
from storyweb.util import make_id


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '<User(%r)>' % (self.id)


class Block(db.Model):
    id = db.Column(db.Unicode(40), primary_key=True, default=make_id)

    def __repr__(self):
        return '<Block(%r)>' % (self.id)






