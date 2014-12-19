from lxml.html.clean import Cleaner

TAGS = ['br', 'p', 'hr', 'b', 'strong', 'em', 'i', 'a',
        'blockquote', 'ul', 'li']
ATTRS = ['href', 'target']

cleaner = Cleaner(style=False, links=True, add_nofollow=False,
                  page_structure=False, safe_attrs_only=True,
                  remove_unknown_tags=False, comments=False,
                  safe_attrs=ATTRS, allow_tags=TAGS)


def clean_html(html):
    if html is None or not len(html):
        return '<p></p>'
    return cleaner.clean_html(html)
