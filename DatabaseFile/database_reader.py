import warnings

import pandas as pd
from pandas import DataFrame
from pandas.errors import ParserWarning

from DatabaseFile.database_file import DatabaseFile


class DatabaseReader:
    def __init__(self, file_path: str):
        self.file = DatabaseFile(file_path)

    def get_database_as_dataframe(self) -> pd.DataFrame:
        # try:
        csv_file: DataFrame = self.__get_csv_with_custom_delimiter_turning_warnings_into_errors()
        return csv_file

    # except Exception as invalid_database_format:
    #     # TODO: we have a write_invalid_file_hash_to_logs() function to use when this exception is raised.
    #     # Figure out if we somehow want to catch it here or in the caller of this function.
    #     raise invalid_database_format

    def __get_csv_with_custom_delimiter_turning_warnings_into_errors(self) -> DataFrame:
        # Hack to turn warnings into errors.
        with warnings.catch_warnings():
            warnings.simplefilter("error", category=ParserWarning)
            csv_file = pd.read_csv(self.file.get_file_path(), engine='python', sep=None, skipinitialspace=True,
                                   index_col=False)
            return csv_file
