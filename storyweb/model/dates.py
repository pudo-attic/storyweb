import logging
from datetime import date
import timestring

log = logging.getLogger(__name__)


class Date(object):

    def __init__(self, value):
        self.value = value

    def to_dict(self):
        return {
            'iso': self.value.isoformat(),
            'year': self.value.year,
            'month': self.value.month,
            'day': self.value.day,
        }

    @property
    def url(self):
        t = (self.value.year, self.value.month, self.value.day)
        return '/dates/%s/%s/%s' % t

    def __eq__(self, other):
        return self.value == other.value

    @classmethod
    def lookup(cls, value):
        if value is None:
            return
        if isinstance(value, date):
            return cls(value)
        try:
            ts = timestring.Date(value)
            return cls(ts.date.date())
        except timestring.TimestringInvalid, inv:
            log.exception(inv)
