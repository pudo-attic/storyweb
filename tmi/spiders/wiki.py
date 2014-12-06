import logging
import wikipedia

from newsclipse.spiders.util import Spider


log = logging.getLogger(__name__)


class Wikipedia(Spider):
    
    def search_all(self, story, card):
        try:
            if card.text is None or not len(card.text.strip()):
                card.text = wikipedia.summary(card.title)
        except wikipedia.WikipediaException, pe:
            log.exception(pe)
