"""
Check fields and data
"""
import unittest

from prospector_holds.models.fields import Field
from prospector_holds.models.leader import Leader


class TestField(unittest.TestCase):

    def test_basic(self):
        line = '001    a'
        field = Field.from_lines((line,), leader=None)
        assert field is not None
        string = str(field)
        assert string == line

    def test_subfield(self):
        subfield = 'This is a test'
        line = '500    |a' + subfield
        field = Field.from_lines((line,), leader=None)
        data = field.data
        assert len(data) == 1
        data = dict(data)
        assert 'a' in data
        assert data['a'] == subfield
        string = str(field)
        assert string == line

    def test_position(self):
        leader = Leader.from_string('LEADER 00000cgm a2201093 i 4500')
        for line in [
            '006    g096#e          ml',
            '007    vd#bsaizm ',
            '008    180102s2018    nyu096 e          vleng d ',
        ]:
            field = Field.from_lines((line,), leader=leader)
            assert len(field.data) > 0


if __name__ == '__main__':
    unittest.main()
