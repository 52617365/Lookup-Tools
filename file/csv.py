import sys
import pandas as pd

from file.file import is_valid_file
from file.file_format import determine_delimiter_from


def read_csv_file(file_path):
    try:
        if not is_valid_file(file_path):
            raise Exception(F"File does not exist: {file_path}")
        file_delimiter = determine_delimiter_from(file_path)
        return pd.read_csv(file_path, delimiter=file_delimiter)
    except Exception as invalid_format:
        raise invalid_format
