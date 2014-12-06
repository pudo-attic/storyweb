import requests
#from pprint import pprint

from tmi.model import Reference, User
from tmi.spiders.util import Spider, text_score

URL = "http://www.openduka.org/index.php/"
API_KEY = '86a6b32f398fe7b3e0a7e13c96b4f032'


class OpenDuka(Spider):

    def make_ref(self, card, id, score, type_, record, idx):
        label = record.get('Citation',
                           record.get('title',
                                      record.get('Name')))
        if len(label) > 80:
            label = label[:80] + '...'
        data = {
            'citation': '%s: %s' % (type_, label),
            'url': URL + 'homes/tree/%s#match%s' % (id, idx),
            'source': 'OpenDuka',
            'score': score,
            'source_url': 'http://openduka.org'
        }
        ref = Reference.find(card, data.get('url'))
        if ref is None:
            ref = Reference()
        ref.save(data, card, User.default_user())
    
    def search_all(self, card):
        args = {'key': API_KEY, 'term': card.title}
        r = requests.get(URL + "api/search", params=args)
        idx = 1
        for match in r.json():
            score = text_score(match.get('Name'), list(card.aliases))
            if score < 50:
                continue
            args = {'key': API_KEY, 'id': match.get('ID')}
            r = requests.get(URL + "api/entity", params=args)
            for type_set in r.json().get('data'):
                for data in type_set['dataset_type']:
                    for type_, ds in data.items():
                        for item in ds:
                            for record in item.get('dataset'):
                                self.make_ref(card, match.get('ID'),
                                              score, type_, record, idx)
                                idx = idx + 1
        return card
