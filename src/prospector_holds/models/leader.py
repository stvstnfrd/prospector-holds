"""
The Leader

There are 24 positions in the Leader,
numbered from 00 to 23.

For fuller explanation,
see the MARC 21 Format for Bibliographic Data [1].

[1] https://www.loc.gov/marc/umb/um07to10.html#part9
"""

from ..settings import SCHEMA_JSON


"""
A magic-word/literal that prefixes the leader line.
"""
LEADER_LITERALS = (
    'LEADER',
    'LDR',
)


def label_to_key(label):
    """
    Convert a label (of space-delimited words) into a dict key

    Assume: label matches the following regex:
        ^[a-zA-Z][-_ a-zA-Z0-9]*$
    """
    key = label
    key = ' '.join(key.split('-'))
    key = '_'.join(key.split(' '))
    key = key.lower()
    return key


class Leader:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        """
        Create a leader line string
        """
        parts = [
            'LEADER ',
        ]
        definition = SCHEMA_JSON['fields']['LDR']
        data = {}
        for offset in sorted(definition['positions'].keys()):
            offsets = offset.split('-')
            if len(offsets) == 1:
                offsets.append(offsets[0])
            start, stop = map(lambda x: int(x, 10), offsets)
            key = label_to_key(definition['positions'][offset]['label'])
            part = getattr(self, key, '')
            len_expected = stop - start + 1
            while len(part) < len_expected:
                part += ' '
            parts.append(part)
        string = ''.join(parts)
        return string

    @classmethod
    def from_string(cls, line):
        """
        Parse a leader line

        e.g. `LEADER 00000cgm a2201093 i 4500 `
        TODO: Assert line is proper length
        """
        line = line.strip()
        parts = line.split(' ', maxsplit=1)
        if not parts[0] in LEADER_LITERALS:
            return None
        line = parts[1]
        definition = SCHEMA_JSON['fields']['LDR']
        data = {}
        for offset in definition['positions'].keys():
            offsets = offset.split('-')
            if len(offsets) == 1:
                offsets.append(offsets[0])
            start, stop = map(lambda x: int(x, 10), offsets)
            value = line[start:stop+1]
            key = label_to_key(definition['positions'][offset]['label'])
            data[key] = value
        instance = cls(**data)
        return instance
