import simplejson
from datetime import datetime, date
from inspect import isgenerator
from flask import Response, request


class AppEncoder(simplejson.JSONEncoder):
    """ This encoder will serialize all entities that have a to_dict
    method by calling that method and serializing the result. """

    #def __init__(self, *a, **kwargs):
        #print (a, kwargs)
        #if 'namedtuple_as_object' in kwargs:
        #    del kwargs['namedtuple_as_object']
    #    super(AppEncoder, self).__init__(*a, **kwargs)

    def default(self, obj):
        if hasattr(obj, 'to_dict'):
            return obj.to_dict()
        elif isinstance(obj, datetime):
            return obj.isoformat() + 'Z'
        elif isinstance(obj, date):
            return obj.isoformat()
        elif isgenerator(obj):
            return [o for o in obj]
        return super(AppEncoder, self).default(self, obj)


def jsonify(obj, status=200, headers=None, index=False, encoder=AppEncoder):
    """ Custom JSONificaton to support obj.to_dict protocol. """
    data = encoder().encode(obj)
    if 'callback' in request.args:
        cb = request.args.get('callback')
        data = '%s && %s(%s)' % (cb, cb, data)
    return Response(data, headers=headers,
                    status=status,
                    mimetype='application/json')
