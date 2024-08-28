"""
Text-based MARC records
"""
from io import StringIO

from .leader import Leader
from .fields import Field


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
                self.leader = Leader.from_string(line)
            else:
                if line[0] == ' ':
                    lines_buffered.append(line)
                else:
                    if len(lines_buffered):
                        field = Field.from_lines(lines_buffered, self.leader)
                        if field:
                            self.fields.append(field)
                    lines_buffered = [line,]
        if len(lines_buffered) > 0:
            field = Field.from_lines(lines_buffered, self.leader)
            if field:
                self.fields.append(field)
            lines_buffered = []

    @property
    def fields_dict(self):
        """
        Represent the fields tuple as a dictionary

        for ease of access/indexing
        """
        data = {}
        for field in self.fields:
            key = field.tag
            value = field
            if key not in data:
                data[key] = []
            data[key].append(value)
        return data

    def __str__(self):
        """
        Serialize a record as text,
        first the leader line, then each of the fields
        """
        lines = [
            str(self.leader)
        ] + [
            str(field)
            for field in self.fields
        ]
        string = '\n'.join(lines)
        return string

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

    @property
    def is_video(self):
        """
        Determine if the record is a video-type asset
        """
        if self.leader.type_of_record == 'g':
            return True
        return False
