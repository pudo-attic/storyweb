from datetime import datetime

from tmi.core import db
from tmi.model.user import User
from tmi.model.card import Card


class Link(db.Model):
    doc_type = 'link'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Unicode)
    
    author_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    author = db.relationship(User, backref=db.backref('links',
                             lazy='dynamic'))

    parent_id = db.Column(db.Integer(), db.ForeignKey('card.id'))
    parent = db.relationship(Card, backref=db.backref('links', lazy='dynamic'),
                             primaryjoin='Card.id==Link.parent_id',
                             )

    child_id = db.Column(db.Integer(), db.ForeignKey('card.id'))
    child = db.relationship(Card, backref=db.backref('linked', lazy='dynamic'),
                            primaryjoin='Card.id==Link.child_id'
                            )

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    def __repr__(self):
        return '<Link(%r,%r,%r)>' % (self.id, self.parent, self.child)

    def to_dict(self):
        return {
            'id': self.id,
            'child': self.child,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }
