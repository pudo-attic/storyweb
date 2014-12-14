import logging
import requests
#from pprint import pprint

from storyweb.core import app
from storyweb.model.card import Card
from storyweb.model.user import User
from storyweb.model.link import Link

log = logging.getLogger(__name__)


def extract_entities(parent):
    from storyweb.queue import index
    for offset, data in extract_calais(parent.text):
        author = User.default_user()
        child = Card.find(data.get('title'))
        if child is None:
            child = Card()
        else:
            data['text'] = child.text
            author = child.author
        child.save(data, author)
        
        if child == parent:
            continue
        data = {
            'offset': offset,
            'child': child
        }
        link = Link.find(parent, child)
        if link is None:
            link = Link()
        else:
            data['status'] = link.status
        link.save(data, parent, author)
    
    index.delay(parent.id)


def extract_calais(text):
    calais_key = app.config.get('CALAIS_KEY')
    if calais_key is None:
        log.warning('No CALAIS_KEY is set, skipping entity extraction')
        return
    if text is None or len(text.strip()) < 10:
        return
    URL = 'http://api.opencalais.com/tag/rs/enrich'
    headers = {
        'x-calais-licenseID': calais_key,
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
            yield offset, data
