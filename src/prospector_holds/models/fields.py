"""
Represent field data of various forms in MARC21 records
"""
from textwrap import wrap

from ..settings import SCHEMA_JSON
from ..utils import label_to_key


class Field:
    """
    A field with a single, unstructured piece of data

    Used by a few lines, mostly/all control lines.
    This is the simplest field type.
    """

    def __init__(self, tag, indicator=None, data=None):
        """
        Create a new field, manually specifying data
        """
        self.tag = tag
        self.indicator = indicator or (' ', ' ')
        self.data = data or tuple()
        definition = SCHEMA_JSON['fields'].get(tag)
        self.repeatable = definition['repeatable']

    def __str__(self):
        """
        Serialize the field as text, as it would appear in a .mrk file.
        """
        indicator = "{indicator1}{indicator2}".format(
            indicator1=self.indicator[0],
            indicator2=self.indicator[1],
        )
        data = self._str_data()
        string = "{tag} {indicator} {data}".format(
            tag=self.tag,
            indicator=indicator,
            data=data,
        )
        return string

    def _str_data(self):
        """
        Create a string of subfield data, as a single, unstructured line
        """
        data = ' '.join(
            value
            for (key, value) in self.data
        )
        return data

    def __repr__(self):
        """
        Create a string representation of the field
        """
        string = "{cls}(tag='{tag}', indicator={indicator}, data={data})".format(
            cls=type(self).__name__,
            tag=self.tag,
            indicator=self.indicator,
            data=self.data,
        )
        return string

    @classmethod
    def from_lines(cls, lines, leader):
        """
        Parse a single field from 1+ lines of text

        from the form:
        ```
        TAG ## ...
        ```
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

        if tag not in SCHEMA_JSON['fields']:
            # TODO: log error
            return None
        definition = SCHEMA_JSON['fields'].get(tag)
        if 'types' in definition:
            data = FieldWithPositions.parse(line, tag, definition, leader)
            _cls = FieldWithPositions
        elif 'subfields' in definition:
            data = FieldWithSubfields.parse(line)
            _cls = FieldWithSubfields
        else:
            data = Field.parse(line)
            _cls = Field
        return _cls(
            tag,
            indicator,
            data,
        )

    @classmethod
    def parse(cls, line):
        """
        Parse text to a field with subfield data

        from the form:
        ```
        plain, unstructured text
        ```
        """
        return (
            (False, line),
        )

class FieldWithSubfields(Field):
    """
    A field with subfield data

    Used by the majority of field tags.
    """

    SUBFIELD_SEPARATOR = '|'

    @classmethod
    def parse(cls, line):
        """
        Parse text to a field with subfield data

        from the form:
        ```
        |asubfield|bsubfield
        ```

        # ASSUME: Sample MARC records appear to (often?) omit the
        # subfield indicator `$a`, if it's the first in the field
        """
        if line[0] != cls.SUBFIELD_SEPARATOR:
            line = cls.SUBFIELD_SEPARATOR + 'a' + line
        fields = line.split(cls.SUBFIELD_SEPARATOR)
        del fields[0]
        subfields = tuple(
            (field[0], field[1:].strip())
            for field in fields
            if field
        )
        return subfields

    def _str_data(self, width=0, separator=None):
        """
        Create a string of subfield data,
        separated by the default separator, '|'.

        Optionally, wrap text to a maximum width.
        """
        if separator is None:
            separator = self.SUBFIELD_SEPARATOR
        data = separator + separator.join(
            key + value
            for (key, value) in self.data
        )
        if width:
            data = wrap(
                data,
                width=width,
                break_on_hyphens=False,
                subsequent_indent='       ',
            )
        else:
            data = (
                data,
            )
        data = ' \n'.join(data)
        return data


class FieldWithPositions(Field):
    """
    A field with positional data

    Only used by a few types of field:
    - 006
    - 007
    - 008
    - LDR
    """

    @classmethod
    def parse(cls, line, tag, definition, leader):
        """
        Parse text to a field with positional data

        from the form:
        ```
        0123456789 abcdefghijklmnopqrstuvwxyz
        ```

        This field type has more edge cases than the others.
        We need to know which tag type we're parsing,
        since 008 fields are context-dependent based on the type of record.
        """
        if tag == '008':
            # Based on the type of record in the leader field,
            # we need to look up the appropriate data type.
            type_of_record = leader.type_of_record
            form_of_material1 = SCHEMA_JSON['fields']['LDR']['positions']['06']['codes'][type_of_record]['label']
            form_of_material2 = None
            for (key, _type) in SCHEMA_JSON['fields']['006']['types'].items():
                if type_of_record in _type['positions']['00']['codes']:
                    form_of_material2 = key
                    break
            if not form_of_material2:
                return None
            _type = dict(definition['types']['All Materials'])
            _type.update(definition['types'][form_of_material2])
        else:  # tag in ('006', '007')
            # For all other tags, we can just look up the data type
            # based on the character in the 00 position.
            types = definition['types']
            types = types.values()
            _type = filter(
                lambda x: line[0] in x['positions'].get('00', {}).get('codes', {}),
                types,
            )
            _type = list(_type)
            if not len(_type):
                return None
            _type = _type[0]
        data = []
        for (offset, subtype) in _type['positions'].items():
            # offset will be either:
            # a single number, zero-padded to 2 digits
            # or a range of two numbers (also zero-padded to 2 digits),
            # separated by a hyphen.
            offsets = offset.split('-')
            if len(offsets) == 1:
                offsets.append(offsets[0])
            start, stop = map(lambda x: int(x, 10), offsets)
            value = line[start:stop+1]
            key = label_to_key(subtype['label'])
            data.append((key, value))
        subfields = tuple(data)
        return subfields

    def _str_data(self):
        """
        Create a string of positional data, each field in order.
        """
        data = ''.join(
            value
            for (key, value) in self.data
        )
        return data
