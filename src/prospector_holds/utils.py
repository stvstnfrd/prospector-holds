"""
General purpose utilities
"""
import re


_REGEX_LABEL_INVALID_CHARACTERS = re.compile(r'[^_a-zA-Z0-9]')
_REGEX_LEADING_NUMBERS = re.compile(r'^[0-9]')
_REGEX_TRAILING_SYMBOLS = re.compile(r'_+$')

def label_to_key(label):
    """
    Convert a label (of space-delimited words) into a dict key

    The key should also be a valid python identifier.
    """
    key = _REGEX_LABEL_INVALID_CHARACTERS.sub('_', label)
    key = key.lower()
    key = _REGEX_TRAILING_SYMBOLS.sub('', key)
    if _REGEX_LEADING_NUMBERS.match(key):
        key = '_' + key
    return key
