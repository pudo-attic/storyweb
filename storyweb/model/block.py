from datetime import datetime
from hashlib import sha1

from storyweb.core import db
from storyweb.model.user import User
from storyweb.model.parser import Renderer, Markdown
from storyweb.model.parser import BlockInlineLexer
from storyweb.model.location import Location
from storyweb.model.entity import Entity
from storyweb.model.dates import Date


class Block(db.Model):
    doc_type = 'block'

    id = db.Column(db.Integer, primary_key=True)
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

    @property
    def signature(self):
        sig = sha1(self.text.encode('utf-8'))
        sig.update(unicode(self.date or ''))
        sig.update(self.source_label or '')
        sig.update(self.source_url or '')
        return sig.hexdigest()

    @property
    def parsed(self):
        sig = self.signature
        if not hasattr(self, '_parsed') or self._parsed[0] != sig:
            renderer = Renderer()
            lexer = BlockInlineLexer(renderer)
            markdown = Markdown(renderer, inline=lexer, escape=True)
            self._parsed = (sig, markdown(self.text), lexer.references)
        return self._parsed[1], self._parsed[2]

    @property
    def html(self):
        return self.parsed[0]

    @property
    def references(self):
        return self.parsed[1]

    def process(self, author):
        locations = set()
        entities = set()
        for ref in self.references:
            if ref['tag'] == 'entity':
                e = ref['label'], ref['type']
                if e not in entities:
                    Entity.lookup(ref['label'], author, type=ref['type'])
                    entities.add(e)

            if ref['tag'] == 'location':
                if ref['text'] not in locations:
                    Location.lookup(ref['text'], author)
                    locations.add(ref['text'])

    @property
    def entities(self):
        if not hasattr(self, '_entities'):
            self._entities = set()
            for ref in self.references:
                if ref['tag'] == 'entity':
                    entity = Entity.by_label(ref['label'], type=ref['type'])
                    self._entities.add(entity)
        return [e for e in self._entities if e is not None]

    @property
    def dates(self):
        if not hasattr(self, '_dates'):
            self._dates = set([Date.lookup(self.date)])
            for ref in self.references:
                if ref['tag'] == 'date':
                    self._dates.add(Date.lookup(ref.get('text')))
        return [e for e in self._dates if e is not None]

    @property
    def locations(self):
        if not hasattr(self, '_locations'):
            self._locations = set()
            for ref in self.references:
                if ref['tag'] == 'location':
                    loc = Location.by_label(ref['text'])
                    self._locations.add(loc)
        return [l for l in self._locations if l is not None]

    def __repr__(self):
        return '<Block(%r)>' % (self.id)

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'html': self.html,
            'source_label': self.source_label,
            'source_url': self.source_url,
            'date': self.date,
            'dates': self.dates,
            'entities': self.entities,
            'locations': self.locations,
            'author': self.author,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

    @classmethod
    def from_dict(cls, data, author):
        block = cls()
        block.text = data.get('text')
        block.date = data.get('date')
        block.source_label = data.get('source_label')
        block.source_url = data.get('source_url')
        block.author = author
        db.session.add(block)
        block.process(author)
        return block
