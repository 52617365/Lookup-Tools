import warnings

import pandas as pd
from pandas import DataFrame
from pandas.errors import ParserWarning

from DatabaseWriter.HashWriter import HashWriter


class DatabaseReader:
    def __init__(self, database_file_path: str, hasher: HashWriter | None, is_json: bool = False):
        self.database_file_path = database_file_path
        self.hasher = hasher
        self.is_json = is_json

    def get_database(self) -> (pd.DataFrame, str):
        file_identifier = self.hasher.get_hash_from_file_contents(self.database_file_path)
        try:
            if self.is_json:
                data_frame = self.get_database_from_json()
                return data_frame, file_identifier
            else:
                data_frame = self.get_database_from_csv()
                return data_frame, file_identifier
        except ParserWarning:
            return pd.DataFrame(), file_identifier

    def get_database_from_csv(self) -> DataFrame:
        # Hack to turn warnings into errors.
        with warnings.catch_warnings():
            warnings.simplefilter("error", category=ParserWarning)
            csv_file = pd.read_csv(self.database_file_path, engine='python', sep='[:;.,\\s+|__]',
                                   index_col=False)
            return csv_file

    def get_database_from_json(self):
        try:
            json_file = pd.read_json(self.database_file_path, lines=True)
            return json_file
        except ValueError:
            raise ParserWarning
