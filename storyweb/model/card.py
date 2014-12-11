import colander
from datetime import datetime
from hashlib import sha1
from sqlalchemy import or_
from sqlalchemy.orm import aliased
from sqlalchemy.ext.associationproxy import association_proxy

from storyweb.core import db, url_for
from storyweb.model.user import User
from storyweb.model.util import db_compare, db_norm
from storyweb.model.forms import Ref


class Alias(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode())
    card_id = db.Column(db.Integer(), db.ForeignKey('card.id'))

    card = db.relationship('Card',
                           backref=db.backref("alias_objects",
                                              cascade="all, delete-orphan"))

    def __init__(self, name):
        self.name = name


class Card(db.Model):
    doc_type = 'card'

    PERSON = 'Person'
    COMPANY = 'Company'
    ORGANIZATION = 'Organization'
    ARTICLE = 'Article'
    CATEGORIES = [PERSON, COMPANY, ORGANIZATION, ARTICLE]

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode)
    category = db.Column(db.Enum(*CATEGORIES))
    text = db.Column(db.Unicode)

    author_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    author = db.relationship(User, backref=db.backref('cards',
                             lazy='dynamic'))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    aliases = association_proxy('alias_objects', 'name')

    def sign(self):
        sig = sha1(self.text.encode('utf-8'))
        sig.update(unicode(self.date or ''))
        sig.update(self.title.encode('utf-8'))
        return sig.hexdigest()

    def __repr__(self):
        return '<Card(%r,%r,%r)>' % (self.id, self.title, self.category)

    def save(self, raw, author):
        from storyweb import queue
        data = CardForm().deserialize(raw)
        self.title = data.get('title', '').strip()
        self.category = data.get('category')
        self.text = data.get('text', '').strip()
        self.date = data.get('date')
        self.aliases = set(data.get('aliases', []) + [data.get('title')])
        self.author = author
        db.session.add(self)
        queue.lookup_all(self.id)
        queue.index.delay(self.id)
        return self

    def to_dict(self):
        return {
            'id': self.id,
            'api_url': url_for('cards_api.view', id=self.id),
            'title': self.title,
            'category': self.category,
            'text': self.text,
            'author': self.author,
            'aliases': self.aliases,
            'references': self.references,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

    def to_index(self):
        data = self.to_dict()
        data.pop('api_url', None)
        data['links'] = []
        for link in self.links:
            ldata = link.to_dict()
            ldata.update(link.child.to_dict())
            ldata.pop('api_url', None)
            ldata.pop('links', None)
            ldata.pop('aliases', None)
            ldata.pop('references', None)
            ldata.pop('author', None)
            ldata.pop('child', None)
            ldata.pop('text', None)
            ldata.pop('created_at', None)
            ldata.pop('updated_at', None)
            data['links'].append(ldata)
        data['references'] = []
        for ref in self.references:
            rdata = ref.to_dict()
            rdata.pop('api_url', None)
            rdata.pop('author', None)
            rdata.pop('created_at', None)
            rdata.pop('updated_at', None)
            data['references'].append(rdata)
        return data

    def __unicode__(self):
        return self.title

    @classmethod
    def suggest(cls, prefix, categories=[]):
        if prefix is None or len(prefix) < 0:
            return []
        c = aliased(cls)
        q = db.session.query(c.id, c.title, c.category)
        prefix = prefix.strip().lower() + '%'
        q = q.filter(db_norm(c.title).like(prefix))
        if len(categories):
            q = q.filter(c.category.in_(categories))
        q = q.limit(10)
        options = []
        for row in q.all():
            options.append({
                'id': row.id,
                'title': row.title,
                'category': row.category
            })
        return options

    @classmethod
    def by_id(cls, id):
        q = db.session.query(cls)
        q = q.filter_by(id=id)
        return q.first()

    @classmethod
    def find(cls, title, category):
        title = title.lower().strip()
        q = db.session.query(cls)
        q = q.outerjoin(Alias)
        q = q.filter(or_(db_compare(cls.title, title),
                         db_compare(Alias.name, title)))
        q = q.filter(cls.category == category)
        return q.first()


class CardRef(Ref):

    def decode(self, data):
        if isinstance(data, Card):
            return data
        if isinstance(data, dict):
            data = data.get('id')
        return Card.by_id(data)


class AliasList(colander.SequenceSchema):
    alias = colander.SchemaNode(colander.String())


class CardForm(colander.MappingSchema):
    title = colander.SchemaNode(colander.String(), default='', missing='')
    category = colander.SchemaNode(colander.String(),
                                   validator=colander.OneOf(Card.CATEGORIES))
    text = colander.SchemaNode(colander.String(), default='', missing='')
    date = colander.SchemaNode(colander.Date(), default=None, missing=None)
    #aliases = AliasList(missing=[], default=[])
