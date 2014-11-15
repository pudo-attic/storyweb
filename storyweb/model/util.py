import string
from uuid import uuid4

ALPHABET = string.ascii_uppercase + string.ascii_lowercase + string.digits


def make_id():
    num = uuid4().int
    s = []
    while True:
        num, r = divmod(num, len(ALPHABET))
        s.append(ALPHABET[r])
        if num == 0:
            break
    return ''.join(reversed(s))

