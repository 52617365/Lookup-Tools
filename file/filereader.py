import os
import csv

import pandas as pd


class FileReader:
    """ FileReader Contract:
    file_path has to be a valid path to a file.
    """

    def __init__(self, file_path_that_exists: str):
        if not self.is_valid_file(file_path_that_exists):
            raise IOError(F"File does not exist: {file_path_that_exists}")
        self.__file_path = file_path_that_exists
        self.__file_name = get_file_without_path_or_extension(file_path_that_exists)

    def get_file_name(self) -> str:
        return self.__file_name

    def get_file_path(self) -> str:
        return self.__file_path

    def get_file_as_csv(self) -> pd.DataFrame:
        try:
            # We specify that the engine is python because the C engine is not able to determine the dynamic delimiter.
            return pd.read_csv(self.__file_path, quoting=csv.QUOTE_NONE, skipinitialspace=True, sep=None,
                               engine='python')
        except Exception as invalid_format:
            raise invalid_format

    @staticmethod
    def is_valid_file(file_path: str):
        return os.path.isfile(file_path)


def get_file_without_path_or_extension(file_name: str) -> str:
    return os.path.splitext(os.path.basename(file_name))[0]


if __name__ == '__main__':
    file_reader = FileReader("../000webhost.com.csv")
    print(file_reader.get_file_as_csv())
