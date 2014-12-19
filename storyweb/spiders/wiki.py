import logging
import wikipedia

from storyweb.spiders.util import Spider


log = logging.getLogger(__name__)


class Wikipedia(Spider):
    
    def search_all(self, card):
        try:
            if card.text is None or not len(card.text.strip()):
                text = wikipedia.summary(card.title)
                if text is not None and len(text):
                    text = text.split('\n', 1)[0]
                    card.text = '<p>%s</p>' % text
        except wikipedia.WikipediaException, pe:
            log.exception(pe)
