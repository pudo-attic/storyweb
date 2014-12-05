
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


CARD_MAPPING = {
    "_id": {
        "path": "id"
    },
    "_all": {
        "enabled": True
    },
    "dynamic": "strict",
    "properties": {
        "id": {"type": "string", "index": "not_analyzed"},
        "title": {"type": "string", "index": "analyzed"},
        "text": {"type": "string", "index": "analyzed"},
        "date": {"type": "date", "index": "not_analyzed"},
        "created_at": {"type": "date", "index": "not_analyzed"},
        "updated_at": {"type": "date", "index": "not_analyzed"},
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
