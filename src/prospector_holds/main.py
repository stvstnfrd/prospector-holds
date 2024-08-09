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
    print(record.leader)
    print(record.fields)


if __name__ == '__main__':
    main()
