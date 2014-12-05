from datetime import datetime
from hashlib import sha1

from tmi.core import db
from tmi.model.user import User


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

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.title,
            'category': self.category,
            'text': self.text,
            'date': self.date,
            'author': self.author,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }
