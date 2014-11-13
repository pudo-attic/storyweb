import json
from uuid import uuid4
import string
from datetime import datetime
from inspect import isgenerator

from flask import Response, request

ALPHABET = string.ascii_uppercase + string.ascii_lowercase + string.digits


class JSONEncoder(json.JSONEncoder):
    """ This encoder will serialize all entities that have a to_dict
    method by calling that method and serializing the result. """

    def __init__(self, index=False):
        self.index = index
        super(JSONEncoder, self).__init__()

    def default(self, obj):
        if hasattr(obj, 'to_dict'):
            return obj.__json__()
        if isinstance(obj, datetime):
            return obj.isoformat() + 'Z'
        if isgenerator(obj):
            return [o for o in obj]
        return json.JSONEncoder.default(self, obj)


def jsonify(obj, status=200, headers=None, index=False, encoder=JSONEncoder):
    """ Custom JSONificaton to support obj.to_dict protocol. """
    if encoder is JSONEncoder:
        data = encoder(index=index).encode(obj)
    else:
        data = encoder().encode(obj)
    if 'callback' in request.args:
        cb = request.args.get('callback')
        data = '%s && %s(%s)' % (cb, cb, data)
    return Response(data, headers=headers,
                    status=status,
                    mimetype='application/json')


def make_id():
    num = uuid4().int
    s = []
    while True:
        num, r = divmod(num, len(ALPHABET))
        s.append(ALPHABET[r])
        if num == 0:
            break
    return ''.join(reversed(s))

