import logging
import requests
from slugify import slugify
from datetime import datetime
from sqlalchemy import func

from storyweb.core import db
from storyweb.model.util import JSONEncodedDict
from storyweb.model.user import User

log = logging.getLogger(__name__)


def geocode(query):
    try:
        URL = 'http://open.mapquestapi.com/nominatim/v1/search.php'
        params = {
            'q': query,
            'format': 'json',
            'addressdetails': 1,
            'limit': 1,
            'accept-language': 'en'
        }
        res = requests.get(URL, params=params)
        data = res.json()
        if data is not None and len(data):
            data = data[0]
            if data.get('importance') > 0.5:
                return data
    except Exception, e:
        log.exception(e)


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.Unicode)
    is_geocoded = db.Column(db.Boolean, default=False)
    country_code = db.Column(db.Unicode)
    country = db.Column(db.Unicode)
    state = db.Column(db.Unicode)
    county = db.Column(db.Unicode)
    city = db.Column(db.Unicode)
    raw = db.Column(JSONEncodedDict)

    author_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    author = db.relationship(User, backref=db.backref('locations',
                             lazy='dynamic'))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    def geocode(self):
        if self.is_geocoded:
            return
        loc = geocode(self.label)
        self.is_geocoded = True
        if loc is None:
            return
        self.raw = loc.get('address', {})
        self.country_code = self.raw.get('country_code')
        if self.country_code is not None:
            self.country_code = self.country_code.upper()
        self.country = self.raw.get('country')
        self.state = self.raw.get('state') or \
            self.raw.get('state_district')
        self.state = self.raw.get('county')
        self.city = self.raw.get('city') or \
            self.raw.get('locality') or \
            self.raw.get('village')
    
    @property
    def url(self):
        # FIXME
        return '/locations/%s-%s' % (self.id, slugify(self.label))

    def __repr__(self):
        return '<Location(%r)>' % (self.id)

    def to_dict(self):
        return {
            'id': self.id,
            'label': self.label,
            'is_geocoded': self.is_geocoded,
            'country_code': self.country_code,
            'country': self.country,
            'state': self.state,
            'county': self.county,
            'city': self.city,
            #'created_at': self.created_at,
            #'updated_at': self.updated_at,
        }

    @classmethod
    def by_label(cls, label):
        if label is None:
            return None
        q = db.session.query(cls)
        q = q.filter(func.trim(func.lower(cls.label)) ==
                     label.lower().strip())
        return q.first()

    @classmethod
    def lookup(cls, label, author):
        log.info('Looking up: %s', label)
        location = cls.by_label(label)
        if location is None and author is not None:
            location = cls()
            location.label = label
            location.author = author
            location.geocode()
            db.session.add(location)
        return location

