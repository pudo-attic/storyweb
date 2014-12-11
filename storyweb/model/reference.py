import colander
from datetime import datetime

from storyweb.core import db, url_for
from storyweb.model.user import User
from storyweb.model.card import Card


class Reference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer)
    citation = db.Column(db.Unicode)
    url = db.Column(db.Unicode)
    source = db.Column(db.Unicode)
    source_url = db.Column(db.Unicode)

    author_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    author = db.relationship(User, backref=db.backref('references',
                             lazy='dynamic'))

    card_id = db.Column(db.Integer(), db.ForeignKey('card.id'))
    card = db.relationship(Card, backref=db.backref('references',
                           lazy='dynamic', order_by='Reference.score.desc()'))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    def save(self, raw, card, author):
        data = ReferenceForm().deserialize(raw)
        self.score = data.get('score')
        self.citation = data.get('citation')
        self.url = data.get('url')
        self.source = data.get('source')
        self.source_url = data.get('source_url')
        self.card = card
        self.author = author
        db.session.add(self)
        return self

    def to_dict(self):
        return {
            'id': self.id,
            'api_url': url_for('references_api.view',
                               card_id=self.card_id, id=self.id),
            'citation': self.citation,
            'url': self.url,
            'score': self.score,
            'source': self.source,
            'source_url': self.source_url,
            'author': self.author,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

    @classmethod
    def by_id(cls, id, card_id=None):
        q = db.session.query(cls)
        q = q.filter_by(id=id)
        if card_id is not None:
            q = q.filter_by(card_id=card_id)
        return q.first()

    @classmethod
    def find(cls, card, url):
        q = db.session.query(cls)
        q = q.filter_by(card=card)
        q = q.filter_by(url=url)
        return q.first()

    def __repr__(self):
        return '<Reference(%r,%r,%r)>' % (self.id, self.citation, self.url)

    def __unicode__(self):
        return self.citation


class ReferenceForm(colander.MappingSchema):
    score = colander.SchemaNode(colander.Int())
    citation = colander.SchemaNode(colander.String())
    url = colander.SchemaNode(colander.String(), validator=colander.url)
    source = colander.SchemaNode(colander.String())
    source_url = colander.SchemaNode(colander.String(), validator=colander.url)
