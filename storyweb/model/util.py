import string
from uuid import uuid4
import json

from sqlalchemy.types import TypeDecorator, VARCHAR
from sqlalchemy.ext.mutable import Mutable

ALPHABET = string.ascii_uppercase + string.ascii_lowercase + string.digits


def make_id():
    num = uuid4().int
    s = []
    while True:
        num, r = divmod(num, len(ALPHABET))
        s.append(ALPHABET[r])
        if num == 0:
            break
    return ''.join(reversed(s))


class JSONEncodedDict(TypeDecorator):
    "Represents an immutable structure as a json-encoded string."

    impl = VARCHAR

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value


class MutableDict(Mutable, dict):
    @classmethod
    def coerce(cls, key, value):
        "Convert plain dictionaries to MutableDict."

        if not isinstance(value, MutableDict):
            if isinstance(value, dict):
                return MutableDict(value)

            # this call will raise ValueError
            return Mutable.coerce(key, value)
        else:
            return value

    def __setitem__(self, key, value):
        "Detect dictionary set events and emit change events."

        dict.__setitem__(self, key, value)
        self.changed()

    def __delitem__(self, key):
        "Detect dictionary del events and emit change events."

        dict.__delitem__(self, key)
        self.changed()
