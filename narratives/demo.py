# https://github.com/bear/parsedatetime/blob/master/examples/basic.py
import re
from mistune import InlineGrammar, InlineLexer, Renderer, Markdown
import copy

# Snippet syntax
#
# - [[Entity Name]]
# - [!Date or datetime]
# - [@Location]


class BlockReference(object):

    def __init__(self, category, match):
        self.category = category
        self.start = match.start(1)
        self.end = match.start(1)
        self.text = match.group(1)

    def __repr__(self):
        return '<BlockReference(%s,%s)>' % (self.category, self.text)

    def __unicode__(self):
        return self.text


class BlockRenderer(Renderer):

    def entity(self, label):
        return '<a href="#" class="entity">' + label + '</a>'

    def location(self, label):
        return '<span class="location">' + label + '</span>'

    def date(self, label):
        return '<span class="date">' + label + '</span>'


class BlockInlineGrammar(InlineGrammar):
    
    entity = re.compile(
        r'\[\['
        r'([\s\S]+?)'
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

    def output_entity(self, m):
        self.references.append(BlockReference('entity', m))
        return self.renderer.entity(m.group(1))

    def output_location(self, m):
        self.references.append(BlockReference('location', m))
        return self.renderer.location(m.group(1))

    def output_date(self, m):
        self.references.append(BlockReference('date', m))
        return self.renderer.date(m.group(1))


def parse_block(block_text):
    renderer = BlockRenderer()
    lexer = BlockInlineLexer(renderer)
    markdown = Markdown(renderer, inline=lexer, escape=True)
    return markdown(block_text), lexer.references


if __name__ == "__main__":
    import sys
    with open(sys.argv[1], 'r') as fh:
        blocks = fh.read().split('\n---\n')
        for block in blocks:
            html, refs = parse_block(block)
            print refs
