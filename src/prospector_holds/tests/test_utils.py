"""
Test the utility functions
"""
import re
import unittest

from prospector_holds.settings import SCHEMA_JSON
from prospector_holds.utils import label_to_key


def _get_labels(data):
    """
    Recursively search a dictionary for all values with the key 'label'
    """
    for key, value in data.items():
        if key == 'label':
            yield value
        elif isinstance(value, dict):
            for _value in _get_labels(value):
                yield _value

class TestUtils(unittest.TestCase):
    REGEX_LABEL = re.compile(r'^[_a-zA-Z][_a-zA-Z0-9]*$')

    def test_label_to_key(self):
        """
        Ensure we never create a key that cannot be a valid python
        identifier

        Check against every possible label in the schema
        """
        labels = _get_labels(SCHEMA_JSON)
        for label in labels:
            key = label_to_key(label)
            assert self.REGEX_LABEL.match(key)


if __name__ == '__main__':
    unittest.main()
