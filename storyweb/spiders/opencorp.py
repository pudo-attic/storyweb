import logging
from urlparse import urljoin
from itertools import count
import requests
#from pprint import pprint

from storyweb.core import app
from storyweb.model import Reference, User
from storyweb.spiders.util import Spider, text_score

log = logging.getLogger(__name__)
API_HOST = 'https://api.opencorporates.com/'
CORP_ID = 'https://opencorporates.com/companies/'


def opencorporates_get(path, query):
    abs_url = path.startswith('http:') or path.startswith('https:')
    url = path if abs_url else urljoin(API_HOST, path)
    params = {'per_page': 200}
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

    def make_query(self, query):
        query = {'q': query}
        api_token = app.config.get('OPENCORPORATES_KEY')
        if api_token is not None and len(api_token):
            query['api_token'] = api_token
        else:
            log.warning('No OPENCORPORATES_KEY is set')
        return query

    def search_company(self, card):
        query = self.make_query(card.title)
        failures = 0
        for company in opencorporates_paginate('companies/search', 'companies',
                                               'company', query):
            url = company.get('opencorporates_url')
            score = text_score(company.get('name'), list(card.aliases))
            if score < 70:
                failures += 1
                continue
            else:
                failures = 0

            if failures > 3:
                break

            citation = 'Company record: %s' % company.get('name')
            self.make_ref(card, score, url, citation)
        return self.search_person(card)

    def search_person(self, card):
        query = self.make_query(card.title)
        failures = 0
        for officer in opencorporates_paginate('officers/search', 'officers',
                                               'officer', query):
            url = officer.get('opencorporates_url')
            score = text_score(officer.get('name'), list(card.aliases))
            if score < 70:
                failures += 1
                continue
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
