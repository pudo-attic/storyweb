import re
from unicodedata import normalize as ucnorm, category

REMOVE_SPACES = re.compile(r'\s+')


def normalize(text):
    if not isinstance(text, unicode):
        text = unicode(text)
    chars = []
    for char in ucnorm('NFKD', text):
        cat = category(char)[0]
        if cat in ['C', 'Z', 'S']:
            chars.append(u' ')
        elif cat in ['M', 'P']:
            continue
        else:
            chars.append(char)
    text = u''.join(chars)
    text = REMOVE_SPACES.sub(' ', text)
    text = text.strip().lower()
    #return ucnorm('NFKC', text)
    return text
