"""
The Leader

There are 24 positions in the Leader,
numbered from 00 to 23.

For fuller explanation,
see the MARC 21 Format for Bibliographic Data [1].

[1] https://www.loc.gov/marc/umb/um07to10.html#part9
"""

"""
A magic-word/literal that prefixes the leader line.
"""
LEADER_LITERAL = 'LEADER '

"""
The fields that compose a leader line.
NOTE: The order of the fields matters;
      they must appear in the same order in code
      as they do in the text.
"""
LEADER_FIELDS = (
    ('header', len(LEADER_LITERAL), str),

    # 00-04 Record length
    # (calculated by the computer for each record)
    ('record_length', 5, int),

    # 05-05 Record status
    #     a: increase in encoding level
    #     c: corrected or revised
    #     d: deleted
    #     n: new
    #     p: increase in encoding from prepublication (previous CIP)
    ('record_status', 1, str),

    # 06-06 Type of record
    #     a: language material
    #     c: printed music
    #     d: manuscript music
    #     e: cartographic material
    #     f: manuscript cartographic material
    #     g: projected medium
    #     i: nonmusical sound recording
    #     j: musical sound recording
    #     k: 2-dimensional nonprojectable graphic
    #     m: computer file
    #     o: kit
    #     p: mixed materials
    #     r: 3-dimensional artifact or naturally occurring object
    #     t: manuscript language material
    ('record_type', 1, str),

    # 07-07 Bibliographic level
    #     a: monographic component part
    #     b: serial component part
    #     c: collection
    #     d: subunit
    #     i: integrating resource
    #     m: monograph/item
    #     s: serial
    ('bibliographic_level', 1, str),

    # 08-08 Type of control
    #     #: no specified type
    #     a: archival
    ('control_type', 1, str),

    # 09-09 Character coding scheme
    #     #: MARC-8
    #     a: UCS/Unicode
    ('character_coding_scheme', 1, str),

    # 10-10 Indicator count
    # (always "2")
    ('indicator_count', 1, int),

    # 11-11 Subfield code count
    # (always "2")
    ('subfield_code_count', 1, int),

    # 12-16 Base address of data
    # (calculated by the computer for each record)
    ('base_address_of_data', 5, int),

    # 17-17 Encoding level
    #     #: full level
    #     1: full level, material not examined
    #     2: less-than-full level, material not examined
    #     3: abbreviated level
    #     4: core level
    #     5: partial (preliminary) level
    #     7: minimal level
    #     8: prepublication level (CIP)
    #     u: unknown
    #     z: not applicable
    ('encoding_level', 1, str),

    # 18-18 Descriptive cataloging form
    #     #: non-ISBD
    #     a: AACR2
    #     i: ISBD
    #     u: unknown
    ('descriptive_cataloging_form', 1, str),

    # 19-19 Multipart resource record level
    #     #: Not specified or not applicable
    #     a: Set
    #     b: Part with independent title
    #     c: Part with dependent title
    ('multipart_resource_level', 1, str),

    # 20-20 Length of the length-of-field portion
    # (always "4")
    ('length_of_length_of_field_portion', 1, str),

    # 21-21 Length of the starting-character-position portion
    # (always "5")
    ('length_of_starting_character_position_portion', 1, str),

    # 22-22 Length of the implementation-defined portion
    # (always "0")
    ('length_of_implementation_defined_porition', 1, str),

    # 23-23 Undefined
    # (always "0")
    ('undefined', 1, str),
)

def parse_leader(line):
    """
    Parse a leader line
    """
    if not line.startswith(LEADER_LITERAL):
        return None
    offset = 0
    data = {}
    for field in LEADER_FIELDS:
        key, length, _type = field
        value = line[offset:offset+length]
        try:
            value = _type(value)
        except ValueError:
            if _type == int:
                value = 0
            elif _type == str:
                value = ''
            else:
                value = None
        offset += length
        data[key] = value
    return data
