from datetime import datetime
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from storyweb.core import db, login_manager
from storyweb.util import make_id


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Unicode)
    display_name = db.Column(db.Unicode)
    password_hash = db.Column(db.Unicode)
    is_admin = db.Column(db.Unicode)
    is_editor = db.Column(db.Unicode)
    active = db.Column(db.Boolean, nullable=False, default=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def is_active(self):
        return self.active

    def is_authenticated(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User(%r)>' % (self.id)


class Block(db.Model):
    id = db.Column(db.Unicode(40), primary_key=True, default=make_id)
    text = db.Column(db.Unicode)
    source_label = db.Column(db.Unicode)
    source_url = db.Column(db.Unicode)
    date = db.Column(db.DateTime)

    author_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    author = db.relationship(User, backref=db.backref('blocks',
                             lazy='dynamic'))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    def __repr__(self):
        return '<Block(%r)>' % (self.id)


class Reference(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    label = db.Column(db.Unicode)
    value = db.Column(db.Unicode)
    category = db.Column(db.Unicode)
    start = db.Column(db.Integer)
    end = db.Column(db.Integer)

    block_id = db.Column(db.Unicode(40), db.ForeignKey('block.id'))
    block = db.relationship(Block, backref=db.backref('references',
                            lazy='dynamic'))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    def __repr__(self):
        return '<Reference(%r)>' % (self.id)



db.create_all()
if db.session.query(User).count() == 0:
    user = User()
    user.email = 'admin@storyweb'
    user.password = 'admin'
    user.display_name = 'Administrator'
    db.session.add(user)
    db.session.commit()

