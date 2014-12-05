import logging
from pyelasticsearch.exceptions import ElasticHttpNotFoundError

from tmi.core import es, es_index
from tmi.util import AppEncoder
from tmi.model.card import Card
from tmi.model.mapping import CARD_MAPPING

log = logging.getLogger(__name__)


class ESResultProxy(object):
    """ This is required for the pager to work. """

    def __init__(self, doc_type, query):
        self.doc_type = doc_type
        self.query = query
        self._limit = 10
        self._offset = 0

    def limit(self, num):
        self._limit = num
        return self

    def offset(self, num):
        self._offset = num
        return self

    @property
    def result(self):
        if not hasattr(self, '_result'):
            q = self.query.copy()
            q['from'] = self._offset
            q['size'] = self._limit
            self._result = es.search(index=es_index,
                                     doc_type=self.doc_type,
                                     query=q)
        return self._result

    def __len__(self):
        return self.result.get('hits', {}).get('total')

    def __iter__(self):
        for hit in self.result.get('hits', {}).get('hits', []):
            res = hit.get('_source')
            res['score'] = hit.get('_score')
            yield res


def init_elasticsearch():
    try:
        es.delete_index(es_index)
    except ElasticHttpNotFoundError:
        pass
    es.create_index(es_index)
    log.info("Creating ElasticSearch index and uploading mapping...")
    es.put_mapping(es_index, Card.doc_type, {Card.doc_type: CARD_MAPPING})


def index_card(card):
    es.json_encoder = AppEncoder
    es.index(es_index, Card.doc_type, card)


def search_cards(query):
    return ESResultProxy(Card.doc_type, query)
