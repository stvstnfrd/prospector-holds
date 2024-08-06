"""
Text-based MARC records
"""
from io import StringIO

from .leader import parse_leader


class MarcRecordText:
    """
    Text-based MARC records
    """

    def __init__(self, stream):
        """
        Create a new record object from a text stream
        """
        self._text = None
        self.leader = None
        for line in stream.readlines():
            line = line.rstrip()
            if not self.leader:
                self.leader = parse_leader(line)

    @classmethod
    def from_string(cls, input_text):
        """
        Create a new record object from a text string
        """
        instance = None
        with StringIO(input_text) as stream:
            instance = cls(stream)
        return instance

    @classmethod
    def from_file(cls, input_file):
        """
        Create a new record object from a text file
        """
        instance = None
        with open(input_file, 'r') as stream:
            instance = cls(stream)
        return instance
