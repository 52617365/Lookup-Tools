import os
import warnings

import pandas as pd
from pandas import DataFrame
from pandas.errors import ParserWarning


class FileReader:
    def __init__(self, file_path: str):
        self.__raise_io_error_if_file_does_not_exist(self, file_path)
        self.__file_path: str = file_path
        self.__file_name: str = self.__get_file_without_path_or_extension(file_path)

    @staticmethod
    def __raise_io_error_if_file_does_not_exist(self, file_path: str):
        if not self.__is_valid_file(file_path):
            raise IOError(F"File does not exist: {file_path}")

    @staticmethod
    def __is_valid_file(file_path: str) -> bool:
        return os.path.isfile(file_path)

    @staticmethod
    def __get_file_without_path_or_extension(file_name: str) -> str:
        return os.path.splitext(os.path.basename(file_name))[0]

    def get_file_name(self) -> str:
        return self.__file_name

    def get_file_as_dataframe(self) -> pd.DataFrame:
        try:
            csv_file: DataFrame = self.__get_csv_with_custom_delimiter_turning_warnings_into_errors()
            return csv_file
        except Exception as invalid_format:
            # TODO: we have a write_invalid_file_hash_to_logs() function to use when this exception is raised.
            # Figure out if we somehow want to catch it here or in the caller of this function.
            raise invalid_format

    def __get_csv_with_custom_delimiter_turning_warnings_into_errors(self) -> DataFrame:
        # Only the python engine can determine a dynamic delimiter.
        # To my knowledge, python engine will only throw a warning, not an error. We want to catch that error.
        with warnings.catch_warnings():
            warnings.simplefilter("error", category=ParserWarning)
            csv_file = pd.read_csv(self.__file_path, engine='python', sep=None, skipinitialspace=True,
                                   index_col=False)
            return csv_file


def get_absolute_path_to_file_from_root(relative_path_to_file_from_root: str) -> str:
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    absolute_path = os.path.join(root_dir, relative_path_to_file_from_root)
    return absolute_path
