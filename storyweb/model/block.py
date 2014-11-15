from datetime import datetime

from storyweb.core import db
from storyweb.model.util import make_id
from storyweb.model.user import User


class Block(db.Model):
    id = db.Column(db.Unicode(40), primary_key=True, default=make_id)
    text = db.Column(db.Unicode)
    source_label = db.Column(db.Unicode)
    source_url = db.Column(db.Unicode)
    date = db.Column(db.Date)

    author_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    author = db.relationship(User, backref=db.backref('blocks',
                             lazy='dynamic'))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    def __repr__(self):
        return '<Block(%r)>' % (self.id)

    @classmethod
    def from_dict(cls, data, author):
        block = cls()
        block.text = data.get('text')
        block.date = data.get('date')
        block.source_label = data.get('source_label')
        block.source_url = data.get('source_url')
        block.authro = author
        db.session.add(block)
        return block


class Reference(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    label = db.Column(db.Unicode)
    value = db.Column(db.Unicode)
    category = db.Column(db.Unicode)
    start = db.Column(db.Integer)
    end = db.Column(db.Integer)

    block_id = db.Column(db.Unicode(40), db.ForeignKey('block.id'))
    block = db.relationship(Block, backref=db.backref('references',
                            lazy='dynamic'))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    def __repr__(self):
        return '<Reference(%r)>' % (self.id)
