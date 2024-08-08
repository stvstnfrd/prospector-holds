"""
Text-based MARC records
"""
from io import StringIO

from .leader import parse_leader


def parse_field(lines):
    """
    Parse a single field from 1+ lines of text
    """
    # Ensure there is at least 1 line of text
    if not lines:
        return None
    # Remove _leading_ whitespace from all lines
    lines = map(str.lstrip, lines)
    # Join all lines together;
    # ASSUME: Each line has appropriate _trailing_ whitespace
    line = ''.join(lines)
    # Remove _trailing_ whitespace from the singular line
    line = line.rstrip()
    # Fields must contain a sequence of:
    #    - one 3-digit tag
    #    - one space character
    #    - two 1-character indicators
    #    - one space character
    # TODO: Is any body required?
    if not line or len(line) < 8:
        return None
    tag = line[0:3]
    indicator = (line[4], line[5])
    line = line[7:]
    fields = line.split('|')
    if fields[0]:
        # ASSUME: Prospector MARC records appear to (often?) omit the
        # subfield indicator `$a`, if it's the first in the field
        fields[0] = 'a' + fields[0]
    else:
        del fields[0]
    subfields = (
        (field[0], field[1:].strip())
        for field in fields
        if field
    )
    subfields = tuple(subfields)
    return (
        tag,
        indicator,
        subfields,
    )


class MarcRecordText:
    """
    Text-based MARC records
    """

    def __init__(self, stream):
        """
        Create a new record object from a text stream
        """
        self.leader = None
        lines_buffered = []
        self.fields = []
        for line in stream.readlines():
            line = line.rstrip('\r\n')
            if not line:
                continue
            if not self.leader:
                self.leader = parse_leader(line)
            else:
                if line[0] == ' ':
                    lines_buffered.append(line)
                else:
                    if len(lines_buffered):
                        field = parse_field(lines_buffered)
                        if field:
                            self.fields.append(field)
                    lines_buffered = [line,]
        if len(lines_buffered) > 0:
            field = parse_field(lines_buffered)
            if field:
                self.fields.append(field)
            lines_buffered = []

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
