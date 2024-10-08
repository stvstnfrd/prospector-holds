"""
The main entrypoint for the package
"""
from prospector_holds.models.record import MarcRecordText


def main():
    """
    Just grab a test file, open it, and take a look.
    """
    input_file = 'test/night-of-the-living-dead-1968.mrk'
    record = MarcRecordText.from_file(input_file)
    print(record)
    print(repr(record.leader))
    for field in record.fields:
        print(repr(field))


if __name__ == '__main__':
    main()
