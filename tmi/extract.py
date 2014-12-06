import requests
#from pprint import pprint

from tmi.core import CALAIS_KEY
from tmi.model import Card, User


def extract_entities(text):
    if text is None or len(text.strip()) < 10:
        return
    URL = 'http://api.opencalais.com/tag/rs/enrich'
    headers = {
        'x-calais-licenseID': CALAIS_KEY,
        'content-type': 'text/raw',
        'accept': 'application/json',
        'enableMetadataType': 'SocialTags'
    }
    res = requests.post(URL, headers=headers,
                        data=text.encode('utf-8'))
    data = res.json()
    for k, v in data.items():
        _type = v.get('_type')
        if _type in ['Person', 'Organization', 'Company']:
            aliases = set([v.get('name')])
            for instance in v.get('instances', [{}]):
                alias = instance.get('exact')
                if alias is not None and len(alias) > 3:
                    aliases.add(alias)

            offset = v.get('instances', [{}])[0].get('offset')
            data = {
                'title': v.get('name'),
                'aliases': list(aliases),
                'category': _type,
                'text': ''
            }
            author = User.default_user()
            card = Card.find(v.get('name'), _type)
            if card is None:
                card = Card()
            else:
                data['text'] = card.text
                author = card.author
            card.save(data, author)
            yield offset, card
