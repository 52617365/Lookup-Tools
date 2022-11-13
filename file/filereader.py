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
            csv_file: DataFrame = self.get_csv_with_custom_delimiter_turning_warnings_into_errors()
            return csv_file
        except Exception as invalid_format:
            # TODO: mark the file as invalid somehow.
            # Maybe have another hash file that contains the hashes to invalid files.
            # We want to handle that here to avoid passing exceptions around.
            raise invalid_format

    def get_csv_with_custom_delimiter_turning_warnings_into_errors(self) -> DataFrame:
        # Only the python engine can determine a dynamic delimiter.
        # To my knowledge, python engine will only throw a warning, not an error. We want to catch that error.
        with warnings.catch_warnings():
            warnings.simplefilter("error", category=ParserWarning)
            csv_file = pd.read_csv(self.__file_path, engine='python', sep=None, skipinitialspace=True,
                                   index_col=False)
            return csv_file
