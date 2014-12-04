from datetime import datetime
from hashlib import sha1

from tmi.core import db
from tmi.model.user import User
from tmi.model.parser import Renderer, Markdown
from tmi.model.parser import BlockInlineLexer
from tmi.model.dates import Date


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

    def sign(self):
        sig = sha1(self.text.encode('utf-8'))
        sig.update(unicode(self.date or ''))
        sig.update(self.source_label or '')
        sig.update(self.source_url or '')
        return sig.hexdigest()

    def parse(self, author=None):
        renderer = Renderer()
        lexer = BlockInlineLexer(renderer, author=author)
        markdown = Markdown(renderer, inline=lexer, escape=True)
        return markdown(self.text), lexer

    @property
    def parsed(self):
        sig = self.sign()
        if not hasattr(self, '_parsed') or self._parsed[0] != sig:
            html, lexer = self.parse()
            self._parsed = (sig, html, lexer)
        return self._parsed[1], self._parsed[2]

    @property
    def html(self):
        return self.parsed[0]

    def process(self, author):
        self.parse(author=author)

    @property
    def entities(self):
        return self.parsed[1].entities

    @property
    def dates(self):
        dates = self.parsed[1].dates
        date = Date.lookup(self.date)
        if date is not None:
            dates.add(date)
        return dates

    @property
    def locations(self):
        return self.parsed[1].locations

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
