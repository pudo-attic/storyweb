import logging
from flask.ext import migrate

from storyweb.model import make_fixtures
from storyweb.search import init_search, reindex


log = logging.getLogger(__name__)


def upgrade():
    log.info("Beginning database migration...")
    migrate.upgrade()
    log.info("Ensuring database fixtures exist...")
    make_fixtures()
    log.info("Reconfiguring the search index...")
    init_search()
    log.info("Re-indexing any existing database objects...")
    reindex()
