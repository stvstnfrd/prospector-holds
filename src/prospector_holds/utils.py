"""
General purpose utilities
"""

def label_to_key(label):
    """
    Convert a label (of space-delimited words) into a dict key

    Assume: label matches the following regex:
        ^[a-zA-Z][-_/ a-zA-Z0-9]*$
    """
    key = label
    key = ' '.join(key.split('-'))
    key = ' '.join(key.split('/'))
    key = '_'.join(key.split(' '))
    key = key.lower()
    return key
