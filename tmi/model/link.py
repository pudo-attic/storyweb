import colander
from datetime import datetime

from tmi.core import db, url_for
from tmi.model.user import User
from tmi.model.card import Card, CardRef


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

    def save(self, raw, parent, child, author):
        data = LinkForm().deserialize(raw)
        self.status = data.get('status')
        self.child = data.get('child')
        self.parent = parent
        self.author = author
        db.session.add(self)
        return self

    def to_dict(self):
        return {
            'id': self.id,
            'api_url': url_for('links_api.view',
                               parent_id=self.parent_id, id=self.id),
            'status': self.status,
            'child': self.child,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

    @classmethod
    def by_id(cls, id, parent_id=None):
        q = db.session.query(cls)
        q = q.filter_by(id=id)
        if parent_id is not None:
            q = q.filter_by(parent_id=parent_id)
        return q.first()


class LinkForm(colander.MappingSchema):
    status = colander.SchemaNode(colander.String())
    child = colander.SchemaNode(CardRef())
    
