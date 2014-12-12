import colander
from datetime import datetime

from storyweb.core import db, url_for
from storyweb.model.user import User
from storyweb.model.card import Card, CardRef


class Link(db.Model):
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    STATUSES = [PENDING, APPROVED, REJECTED]

    id = db.Column(db.Integer, primary_key=True)
    offset = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(db.Enum(*STATUSES), nullable=False, default=PENDING)
    
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

    def save(self, raw, parent, author):
        data = LinkForm().deserialize(raw)
        self.status = data.get('status')
        self.offset = data.get('offset')
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

    @classmethod
    def find(cls, parent, child):
        q = db.session.query(cls)
        q = q.filter_by(parent=parent)
        q = q.filter_by(child=child)
        return q.first()


class LinkForm(colander.MappingSchema):
    status = colander.SchemaNode(colander.String(), missing=Link.PENDING)
    offset = colander.SchemaNode(colander.Int(), missing=0)
    child = colander.SchemaNode(CardRef())
    
