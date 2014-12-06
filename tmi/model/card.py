import colander
from datetime import datetime
from hashlib import sha1

from tmi.core import db, url_for
from tmi.model.user import User
from tmi.model.forms import Ref


class Card(db.Model):
    doc_type = 'card'
    CATEGORIES = ['Person', 'Company', 'Organization', 'Article']

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode)
    category = db.Column(db.Enum(*CATEGORIES))
    text = db.Column(db.Unicode)
    date = db.Column(db.Date)

    author_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    author = db.relationship(User, backref=db.backref('cards',
                             lazy='dynamic'))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    def sign(self):
        sig = sha1(self.text.encode('utf-8'))
        sig.update(unicode(self.date or ''))
        sig.update(self.title.encode('utf-8'))
        return sig.hexdigest()

    def __repr__(self):
        return '<Card(%r,%r,%r)>' % (self.id, self.title, self.category)

    def save(self, raw, author):
        data = CardForm().deserialize(raw)
        self.title = data.get('title')
        self.category = data.get('category')
        self.text = data.get('text')
        self.date = data.get('date')
        self.author = author
        db.session.add(self)
        return self

    def to_dict(self):
        return {
            'id': self.id,
            'api_url': url_for('cards_api.view', id=self.id),
            'title': self.title,
            'category': self.category,
            'text': self.text,
            'date': self.date,
            'author': self.author,
            #'links': self.links,
            'references': self.references,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

    def __unicode__(self):
        return self.title

    @classmethod
    def by_id(cls, id):
        q = db.session.query(cls)
        q = q.filter_by(id=id)
        return q.first()


class CardRef(Ref):

    def decode(self, data):
        if isinstance(data, Card):
            return data
        if isinstance(data, dict):
            data = data.get('id')
        return Card.by_id(data)


class CardForm(colander.MappingSchema):
    title = colander.SchemaNode(colander.String())
    category = colander.SchemaNode(colander.String(),
                                   validator=colander.OneOf(Card.CATEGORIES))
    text = colander.SchemaNode(colander.String())
    date = colander.SchemaNode(colander.Date(), default=None, missing=None)
