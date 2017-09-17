import re


def match(rx, text):
    if text is None:
        return False
    return re.search(rx, text)
