import logging

from storyweb.model import init_db
from storyweb.search import init_search, reindex


log = logging.getLogger(__name__)


def upgrade():
    init_db()
    init_search()
    log.info("Re-indexing any existing database objects...")
    reindex()
