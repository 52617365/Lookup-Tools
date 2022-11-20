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
        global csv_file
        try:
            csv_file = self.get_database_as_dataframe()
            file_identifier = self.hasher.get_blake2b_hash_from(csv_file)
            return csv_file, file_identifier
        except ParserWarning:
            file_identifier = self.hasher.get_blake2b_hash_from(csv_file)
            return csv_file, file_identifier

    def get_database_as_dataframe(self) -> pd.DataFrame:
        csv_file: DataFrame = self.__get_csv_with_custom_delimiter_turning_warnings_into_errors()
        return csv_file

    # TODO: handle how we're going to be generating the invalid hash if this function fails.
    # currently it's not generating invalid hashes correctly for invalid files. It's because if it fails, we are not correctly generating the hash.
    def __get_csv_with_custom_delimiter_turning_warnings_into_errors(self) -> DataFrame:
        # Hack to turn warnings into errors.
        with warnings.catch_warnings():
            warnings.simplefilter("error", category=ParserWarning)
            csv_file = pd.read_csv(self.database_file_path, engine='python', sep=None,
                                   skipinitialspace=True,
                                   index_col=False)
            return csv_file
