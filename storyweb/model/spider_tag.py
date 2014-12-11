from datetime import datetime

from storyweb.core import db


class SpiderTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    spider = db.Column(db.Unicode)

    card_id = db.Column(db.Integer(), db.ForeignKey('card.id'))
    card = db.relationship('Card')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    def __repr__(self):
        return '<SpiderTag(%r,%r,%r)>' % (self.id, self.card,
                                          self.spider, self.status)

    @classmethod
    def find(cls, card, spider):
        q = db.session.query(cls)
        q = q.filter(cls.card == card)
        q = q.filter(cls.spider == spider)
        return q.first()

    @classmethod
    def done(cls, card, spider):
        obj = cls.find(card, spider)
        if obj is None:
            obj = cls()
            obj.card = card
            obj.spider = spider
        db.session.add(obj)
