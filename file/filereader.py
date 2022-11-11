import os
import csv
import warnings

import pandas as pd
from pandas.errors import ParserWarning


class FileReader:
    def __init__(self, file_path_that_exists: str):
        if not self.is_valid_file(file_path_that_exists):
            raise IOError(F"File does not exist: {file_path_that_exists}")
        self.__file_path = file_path_that_exists
        self.__file_name = get_file_without_path_or_extension(file_path_that_exists)

    def get_file_name(self) -> str:
        return self.__file_name

    def get_file_path(self) -> str:
        return self.__file_path

    def get_file_as_dataframe(self) -> pd.DataFrame:
        try:
            # We specify that the engine is python because the C engine is not able to determine the dynamic delimiter.
            # We have to turn the warning into an error here because the python engine shows a warning instead of an error.
            with warnings.catch_warnings():
                warnings.simplefilter("error", category=ParserWarning)
                csv_file = pd.read_csv(self.__file_path, engine='python', sep=None, skipinitialspace=True, index_col=False)
                return csv_file
        except Exception as invalid_format:
            raise invalid_format

    @staticmethod
    def is_valid_file(file_path: str) -> bool:
        return os.path.isfile(file_path)


def get_file_without_path_or_extension(file_name: str) -> str:
    return os.path.splitext(os.path.basename(file_name))[0]


if __name__ == '__main__':
    file_reader = FileReader("../000webhost.com.csv")
    print(file_reader.get_file_as_dataframe())
