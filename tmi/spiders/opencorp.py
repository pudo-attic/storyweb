# OpenCorporates
#
# http://api.opencorporates.com/documentation/API-Reference
#
#from pprint import pprint
from itertools import count
from tmi.model import Reference, User
from tmi.spiders.util import Spider, text_score
from urlparse import urljoin
import requests

API_HOST = 'https://api.opencorporates.com/'
CORP_ID = 'https://opencorporates.com/companies/'
API_TOKEN = 'Y2t6PVBfvoJTxhsI0ZJf'


def opencorporates_get(path, query):
    url = path if path.startswith('http:') or path.startswith('https:') else urljoin(API_HOST, path)
    params = {'per_page': 200}
    if API_TOKEN is not None:
        params['api_token'] = API_TOKEN
    params.update(query)
    res = requests.get(url, params=params)
    return res.json()


def opencorporates_paginate(path, collection_name, item_name, query):
    res = {}
    for i in count(1):
        if i > res.get('total_pages', 10000):
            return
        res = opencorporates_get(path, query)
        if 'error' in res:
            return
        res = res.get('results', {})
        for data in res.get(collection_name, []):
            data = data.get(item_name)
            yield data


class OpenCorporates(Spider):

    def make_api_url(self, url):
        if '://api.' not in url:
            url = url.replace('://', '://api.')
        return url

    def make_ref(self, card, score, url, citation):
        data = {
            'citation': citation,
            'url': url,
            'source': 'OpenCorporates',
            'score': score,
            'source_url': 'https://opencorporates.com'
        }
        ref = Reference.find(card, data.get('url'))
        if ref is None:
            ref = Reference()
        ref.save(data, card, User.default_user())

    def search_organization(self, card):
        return self.search_company(card)

    def search_company(self, card):
        query = {'q': card.title}
        failures = 0
        for company in opencorporates_paginate('companies/search', 'companies',
                                               'company', query):
            url = company.get('opencorporates_url')
            score = text_score(company.get('name'), list(card.aliases))
            if score < 70:
                failures += 1
            else:
                failures = 0

            if failures > 3:
                break

            citation = 'Company record: %s' % company.get('name')
            self.make_ref(card, score, url, citation)
        return self.search_person(card)

    def search_person(self, card):
        query = {'q': card.title}
        failures = 0
        for officer in opencorporates_paginate('officers/search', 'officers',
                                               'officer', query):
            url = officer.get('opencorporates_url')
            score = text_score(officer.get('name'), list(card.aliases))
            if score < 70:
                failures += 1
            else:
                failures = 0

            if failures > 3:
                break

            corp_data = officer.get('company')
            position = officer.get('position')
            if not position:
                position = 'an officer'
            citation = '%s is %s of %s' % (officer.get('name'),
                                           position,
                                           corp_data.get('name'))
            self.make_ref(card, score, url, citation)
        return card
