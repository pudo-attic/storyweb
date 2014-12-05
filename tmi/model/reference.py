from datetime import datetime

from tmi.core import db
from tmi.model.user import User
from tmi.model.card import Card


class Reference(db.Model):
    doc_type = 'reference'

    id = db.Column(db.Integer, primary_key=True)
    citation = db.Column(db.Unicode)
    url = db.Column(db.Unicode)
    source = db.Column(db.Unicode)
    source_url = db.Column(db.Unicode)

    author_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    author = db.relationship(User, backref=db.backref('references',
                             lazy='dynamic'))

    card_id = db.Column(db.Integer(), db.ForeignKey('card.id'))
    card = db.relationship(Card, backref=db.backref('references',
                           lazy='dynamic'))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    def __repr__(self):
        return '<Reference(%r,%r,%r)>' % (self.id, self.citation, self.url)

    def __unicode__(self):
        return self.citation

    def to_dict(self):
        return {
            'id': self.id,
            'citation': self.citation,
            'url': self.url,
            'date': self.source,
            'author': self.source_url,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }
