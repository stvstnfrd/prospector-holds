"""
Check leader line tests
"""
import unittest


from prospector_holds.models.leader import Leader


class TestLeader(unittest.TestCase):
    INPUT_DATA = (
        ('record_length', '00000'),
        ('record_status', 'c'),
        ('type_of_record', 'g'),
        ('bibliographic_level', 'm'),
        ('type_of_control', ' '),
        ('character_coding_scheme', 'a'),
        ('indicator_count', '2'),
        ('subfield_code_count', '2'),
        ('base_address_of_data', '01093'),
        ('encoding_level', ' '),
        ('descriptive_cataloging_form', 'i'),
        ('multipart_resource_record_level', ' '),
        ('length_of_the_length_of_field_portion', '4'),
        ('length_of_the_starting_character_position_portion', '5'),
        ('length_of_the_implementation_defined_portion', '0'),
        ('undefined', '0'),
    )
    INPUT_LINE = ''.join(('LEADER ',) + tuple(
        expected
        for key, expected in INPUT_DATA
    ))
    INPUT_LINE_WITH_SPACE = ' ' + INPUT_LINE + '   '
    INPUT_LINE_WITH_NEWLINE = ' ' + INPUT_LINE + """   
    """

    def test_create(self):
        line = self.INPUT_LINE
        assert line is not None
        leader = Leader.from_string(line)
        assert leader is not None
        assert str(leader) == self.INPUT_LINE
        for key, expected in self.INPUT_DATA:
            actual = getattr(leader, key)
            assert expected == actual

    def test_create_from_data(self):
        data = {
            key: value
            for key, value in self.INPUT_DATA
        }
        leader = Leader(**data)
        line = str(leader)
        assert line == self.INPUT_LINE
        for key, expected in self.INPUT_DATA:
            actual = getattr(leader, key)
            assert expected == actual

    def test_serialize(self):
        line_input = self.INPUT_LINE
        leader = Leader.from_string(line_input)
        line_output = str(leader)
        assert line_output is not None
        assert line_output == line_input

    def test_serialize_with_space(self):
        line_input = self.INPUT_LINE_WITH_SPACE
        leader = Leader.from_string(line_input)
        line_output = str(leader)
        assert line_output == line_input.strip()

    def test_serialize_with_newline(self):
        line_input = self.INPUT_LINE_WITH_NEWLINE
        leader = Leader.from_string(line_input)
        line_output = str(leader)
        assert line_output == line_input.strip()


if __name__ == '__main__':
    unittest.main()
