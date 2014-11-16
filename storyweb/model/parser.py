import re
from mistune import InlineGrammar, InlineLexer
from mistune import Markdown, Renderer # noqa
import copy

from storyweb.model.location import Location
from storyweb.model.entity import Entity
from storyweb.model.dates import Date

# Snippet syntax
#
# - [[Entity Name|Entity Canonical Name|Entity Type]]
# - [!Date or datetime]
# - [@Location]


class BlockInlineGrammar(InlineGrammar):
    
    entity = re.compile(
        r'\[\['
        r'([\s\S\|]+?)'
        r'\]\](?!\])'
    )

    location = re.compile(
        r'\[@'
        r'([\s\S]+?)'
        r'\]'
    )

    date = re.compile(
        r'\[!'
        r'([\s\S]+?)'
        r'\]'
    )


class BlockInlineLexer(InlineLexer):
    default_features = copy.copy(InlineLexer.default_features)
    default_features.insert(3, 'entity')
    default_features.insert(3, 'date')
    default_features.insert(3, 'location')

    def __init__(self, renderer, author=None, **kwargs):
        rules = BlockInlineGrammar()
        self.author = author
        self.entities = set()
        self.locations = set()
        self.dates = set()
        super(BlockInlineLexer, self).__init__(renderer, rules, **kwargs)

    def parse_entity_tag(self, m):
        label, type = m.group(1), None
        data = label.rsplit('|', 2)
        text = data[0]
        if len(data) > 1 and len(data[1]):
            label = data[1]
        if len(data) > 2 and len(data[2]):
            type = data[2]
        return (text, label, type)

    def output_entity(self, m):
        text, label, type = self.parse_entity_tag(m)
        entity = Entity.lookup(label, self.author, type=type)
        if entity is not None:
            self.entities.add(entity)
            return '<a href="%s" class="entity">%s</a>' % (entity.url, text)
        return '<span class="entity broken">%s</span>' % text

    def output_location(self, m):
        text = m.group(1)
        location = Location.lookup(text, self.author)
        if location is not None:
            self.locations.add(location)
            return '<a href="%s" class="location">%s</a>' % (location.url, text)
        return '<span class="location broken">%s</span>' % text

    def output_date(self, m):
        text = m.group(1)
        date = Date.lookup(text)
        if date is not None:
            self.dates.add(date)
            return '<a href="%s" class="date">%s</a>' % (date.url, text)
        return '<span class="date broken">%s</span>' % text
