import re
import logging
from sqlalchemy.orm import aliased

from storyweb.model import Card, User, Link, Alias, db
from storyweb.analysis.text import normalize
from storyweb.analysis.calais import extract_calais

log = logging.getLogger(__name__)


def card_titles():
    alias = aliased(Alias)
    card = aliased(Card)
    q = db.session.query(alias.name)
    q = q.join(card, alias.card)
    q = q.add_column(card.id)
    to_d = lambda r: {
        'id': r.id,
        'text': r.name,
        'normalized': normalize(r.name)
    }
    return [to_d(r) for r in q.all()]


def extract_known(parent):
    if parent.text is None or not len(parent.text):
        return
    cards = card_titles()
    names = [c['normalized'] for c in cards]
    names = re.compile('(%s)' % '|'.join(names))
    matches = []
    for match in names.finditer(normalize(parent.text)):
        for card in cards:
            if card['normalized'] == match.group(1):
                matches.append((card['id'], match.start(1)))
    
    ids = set([m[0] for m in matches])
    q = db.session.query(Card)
    q = q.filter(Card.id.in_(ids))
    cards = {c.id: c for c in q.all()}

    for id, offset in matches:
        card = cards.pop(id, None)
        if card is not None:
            yield offset, card


def extract_multi(parent):
    seen = set([parent.id])
    for offset, card in extract_known(parent):
        if card.id not in seen:
            seen.add(card.id)
            yield offset, card

    for offset, data in extract_calais(parent.text):
        author = User.default_user()
        card = Card.find(data.get('title'))
        if card is None:
            card = Card()
        elif card.id in seen:
            continue
        else:
            data['text'] = card.text
            author = card.author
        card.save(data, author)
        seen.add(card.id)
        yield offset, card


def extract_entities(parent):
    from storyweb.queue import index
    for offset, child in extract_multi(parent):
        log.info("Extraced: %r in %r", child, parent)
        data = {
            'offset': offset,
            'child': child
        }
        link = Link.find(parent, child)
        if link is None:
            link = Link()
        else:
            data['status'] = link.status
        link.save(data, parent, child.author)
    
    index.delay(parent.id)
