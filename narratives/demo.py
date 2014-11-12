# https://github.com/bear/parsedatetime/blob/master/examples/basic.py
import re
import mistune

# Snippet syntax
#
# - [[Entity Name]]
# - ![Date or datetime]
# - @[Location]


def parse_block(block_text):
    print [block_text]


if __name__ == "__main__":
    import sys
    with open(sys.argv[1], 'r') as fh:
        blocks = fh.read().split('\n---\n')
        for block in blocks:
            parse_block(block)
