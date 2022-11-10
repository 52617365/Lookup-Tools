import csv
import sys
from file.file import is_valid_file


def determine_delimiter_from(file_path):
    first_line_of_file = read_first_line_from_file(file_path)
    try:
        file_delimiter = csv.Sniffer().sniff(first_line_of_file).delimiter
        return file_delimiter
    except (Exception,):
        raise Exception(F"Could not determine file delimiter from line: {first_line_of_file}\n file: {file_path}")


def read_first_line_from_file(file_name):
    if not is_valid_file(file_name):
        print(F"File does not exist: {file_name}")
        sys.exit(1)

    with open(file_name, 'r') as f:
        first_line = f.readline()
        f.close()
        return first_line
