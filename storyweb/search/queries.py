

def cards_query(req):
    qstr = req.get('q', '').strip()
    if len(qstr):
        q = {'query_string': {'query': qstr}}
        bq = [
            {"term": {"title": {"value": qstr, "boost": 10.0}}},
            {"term": {"aliases": {"value": qstr, "boost": 6.0}}},
            {"term": {"text": {"value": qstr, "boost": 3.0}}}
        ]
        q = {
            "bool": {
                "must": q,
                "should": bq
            }
        }
        print q
    else:
        q = {'match_all': {}}
    return {'query': q}
