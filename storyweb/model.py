from werkzeug.security import generate_password_hash, \
     check_password_hash

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
    active = db.Column(db.Boolean, nullable=False, default=True)

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

    def __repr__(self):
        return '<Block(%r)>' % (self.id)


db.create_all()
if db.session.query(User).count() == 0:
    user = User()
    user.email = 'admin@storyweb'
    user.password = 'admin'
    user.display_name = 'Administrator'
    db.session.add(user)
    db.session.commit()

