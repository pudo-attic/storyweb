from datetime import datetime
from hashlib import sha1

from storyweb.core import db
from storyweb.model.util import make_id
from storyweb.model.user import User
from storyweb.model.parser import Renderer, Markdown
from storyweb.model.parser import BlockInlineLexer
from storyweb.model.location import Location
from storyweb.model.entity import Entity


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

    def __repr__(self):
        return '<Block(%r)>' % (self.id)

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
