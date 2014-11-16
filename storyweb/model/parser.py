import re
from mistune import InlineGrammar, InlineLexer
from mistune import Markdown, Renderer # noqa
import copy

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

    def __init__(self, renderer, **kwargs):
        rules = BlockInlineGrammar()
        self.references = []
        super(BlockInlineLexer, self).__init__(renderer, rules, **kwargs)

    def parse_tag(self, m, tag):
        return {
            'tag': tag,
            'text': m.group(1),
            'start': m.start(1),
            'end': m.end(1),
        }

    def output_entity(self, m):
        r = self.parse_tag(m, 'entity')
        data = r['text'].rsplit('|', 2)
        r['text'] = data[0]
        r['label'] = data[0]
        if len(data) > 1 and len(data[1]):
            r['label'] = data[1]
        if len(data) > 2 and len(data[2]):
            r['type'] = data[2]
        self.references.append(r)
        return '<a href="#" class="entity">' + r['text'] + '</a>'

    def output_location(self, m):
        r = self.parse_tag(m, 'location')
        self.references.append(r)
        return '<span class="location">' + r['text'] + '</span>'

    def output_date(self, m):
        r = self.parse_tag(m, 'date')
        self.references.append(r)
        return '<span class="date">' + r['text'] + '</span>'
