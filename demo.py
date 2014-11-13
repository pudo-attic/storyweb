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

    def entity(self, ref):
        return '<a href="#" class="entity">' + ref.text + '</a>'

    def location(self, ref):
        return '<span class="location">' + ref.text + '</span>'

    def date(self, ref):
        return '<span class="date">' + ref.text + '</span>'


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
        r = BlockReference('entity', m)
        self.references.append(r)
        return self.renderer.entity(r)

    def output_location(self, m):
        r = BlockReference('location', m)
        self.references.append(r)
        return self.renderer.location(r)

    def output_date(self, m):
        r = BlockReference('date', m)
        self.references.append(r)
        return self.renderer.date(r)


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
