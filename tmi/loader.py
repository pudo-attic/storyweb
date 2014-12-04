import yaml
from datetime import datetime

from tmi.model import db, Block, User

SEPARATOR = '\n\n---\n\n'


def load_block(block, user):
    block['date'] = datetime.strptime(block['date'], '%Y-%m-%d').date()
    block = Block.from_dict(block, user)


def load(filename):
    user = User.default_user()
    with open(filename, 'r') as fp:
            blocks = fp.read().split(SEPARATOR)
            for block in blocks:
                block = yaml.load(block)
                load_block(block, user)
                db.session.commit()
