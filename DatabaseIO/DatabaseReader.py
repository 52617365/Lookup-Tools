import warnings

import pandas as pd
from pandas import DataFrame
from pandas.errors import ParserWarning

from DatabaseIO.HashWriter import HashWriter


class DatabaseReader:
    def __init__(self, database_file_path: str, hasher: HashWriter):
        self.database_file_path = database_file_path
        self.hasher = hasher

    def get_database(self) -> (pd.DataFrame, str):
        file_identifier = self.hasher.get_hash_from_file_contents(self.database_file_path)
        try:
            csv_file = self.get_database_as_dataframe()
            return csv_file, file_identifier
        except ParserWarning:
            return pd.DataFrame(), file_identifier

    def get_database_as_dataframe(self) -> pd.DataFrame:
        csv_file: DataFrame = self.__get_csv_with_custom_delimiter_turning_warnings_into_errors()
        return csv_file

    def __get_csv_with_custom_delimiter_turning_warnings_into_errors(self) -> DataFrame:
        # Hack to turn warnings into errors.
        with warnings.catch_warnings():
            warnings.simplefilter("error", category=ParserWarning)
            csv_file = pd.read_csv(self.database_file_path, engine='python', sep=None,
                                   skipinitialspace=True,
                                   index_col=False)
            return csv_file
