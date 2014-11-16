import logging
from pyelasticsearch.exceptions import IndexAlreadyExistsError
from pyelasticsearch.exceptions import ElasticHttpNotFoundError

from storyweb.core import es, es_index
from storyweb.util import AppEncoder
from storyweb.model.block import Block

log = logging.getLogger(__name__)

BLOCK_MAPPING = {
    "_id": {
        "path": "id"
    },
    "_all": {
        "enabled": True
    },
    "dynamic": "strict",
    "properties": {
        "id": {"type": "string", "index": "not_analyzed"},
        "text": {"type": "string", "index": "analyzed"},
        "html": {"type": "string", "index": "analyzed"},
        "date": {"type": "date", "index": "not_analyzed"},
        "created_at": {"type": "date", "index": "not_analyzed"},
        "updated_at": {"type": "date", "index": "not_analyzed"},
        "source_label": {"type": "string", "index": "not_analyzed"},
        "source_url": {"type": "string", "index": "not_analyzed"},
        "locations": {
            "_id": {
                "path": "id"
            },
            "type": "nested",
            "include_in_parent": True,
            "properties": {
                "id": {"type": "string", "index": "not_analyzed"},
                "is_geocoded": {"type": "string", "index": "not_analyzed"},
                "label": {"type": "string", "index": "not_analyzed"},
                "country_code": {"type": "string", "index": "not_analyzed"},
                "country": {"type": "string", "index": "not_analyzed"},
                "state": {"type": "string", "index": "not_analyzed"},
                "county": {"type": "string", "index": "not_analyzed"},
                "city": {"type": "string", "index": "not_analyzed"}
            }
        },
        "entities": {
            "_id": {
                "path": "id"
            },
            "type": "nested",
            "include_in_parent": True,
            "properties": {
                "id": {"type": "string", "index": "not_analyzed"},
                "type": {"type": "string", "index": "not_analyzed"},
                "label": {"type": "string", "index": "not_analyzed"}
            }
        },
        "dates": {
            "_id": {
                "path": "iso"
            },
            "type": "nested",
            "include_in_parent": True,
            "properties": {
                "iso": {"type": "string", "index": "not_analyzed"},
                "year": {"type": "string", "index": "not_analyzed"},
                "month": {"type": "string", "index": "not_analyzed"},
                "day": {"type": "string", "index": "not_analyzed"}
            }
        },
        "author": {
            "_id": {
                "path": "id"
            },
            "type": "nested",
            "include_in_parent": True,
            "properties": {
                "id": {"type": "string", "index": "not_analyzed"},
                "display_name": {"type": "string", "index": "not_analyzed"}
            }
        }
    }
}


def init_elasticsearch():
    try:
        es.delete_index(es_index)
    except ElasticHttpNotFoundError:
        pass
    try:
        es.create_index(es_index)
    except IndexAlreadyExistsError:
        pass
    log.info("Creating ElasticSearch index and uploading mapping...")
    es.put_mapping(es_index, Block.doc_type, {Block.doc_type: BLOCK_MAPPING})


def index_block(block):
    es.json_encoder = AppEncoder
    es.index(es_index, Block.doc_type, block)
