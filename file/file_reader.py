import os
import warnings

import pandas as pd
from pandas import DataFrame
from pandas.errors import ParserWarning

from file.file import File


class FileReader:
    def __init__(self, file_path: str):
        self.__file = File(file_path)

    def get_file(self) -> File:
        return self.__file

    def get_file_as_dataframe(self) -> pd.DataFrame:
        # try:
        csv_file: DataFrame = self.__get_csv_with_custom_delimiter_turning_warnings_into_errors()
        return csv_file

    # except Exception as invalid_database_format:
    #     # TODO: we have a write_invalid_file_hash_to_logs() function to use when this exception is raised.
    #     # Figure out if we somehow want to catch it here or in the caller of this function.
    #     raise invalid_database_format

    def __get_csv_with_custom_delimiter_turning_warnings_into_errors(self) -> DataFrame:
        # Only the python engine can determine a dynamic delimiter.
        # To my knowledge, python engine will only throw a warning, not an error. We want to catch that error.
        with warnings.catch_warnings():
            warnings.simplefilter("error", category=ParserWarning)
            csv_file = pd.read_csv(self.__file.get_file_path(), engine='python', sep=None, skipinitialspace=True,
                                   index_col=False)
            return csv_file


def get_absolute_path_to_file_from_root(relative_path_to_file_from_root: str) -> str:
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    absolute_path = os.path.join(root_dir, relative_path_to_file_from_root)
    return absolute_path
