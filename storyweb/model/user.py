from datetime import datetime
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from storyweb.core import db, login_manager


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Unicode)
    display_name = db.Column(db.Unicode)
    password_hash = db.Column(db.Unicode)
    is_admin = db.Column(db.Boolean)
    is_editor = db.Column(db.Boolean)
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
        return '<User(%r,%r)>' % (self.id, self.email)

    def __unicode__(self):
        return self.display_name

    @classmethod
    def default_user(cls):
        q = db.session.query(cls)
        q = q.filter(cls.is_admin == True) # noqa
        q = q.order_by(cls.created_at.asc())
        user = q.first()
        if user is None:
            user = cls()
            user.email = 'admin@grano.cc'
            user.password = 'admin'
            user.display_name = 'Administrator'
            user.is_editor = True
            user.is_admin = True
            db.session.add(user)
        return user
