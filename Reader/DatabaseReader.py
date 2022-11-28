import warnings

import pandas as pd
from pandas import DataFrame
from pandas.errors import ParserWarning

from Format.FileFormatDeterminer import FileFormat
from Reader.Hash import Hash


class DatabaseReader:
    def __init__(self, database_file_path: str, file_format: FileFormat, is_json: bool = False):
        self.database_file_path = database_file_path
        self.file_format = file_format
        self.is_json = is_json
        self.hash = Hash(self.database_file_path)

    def get_database(self) -> (pd.DataFrame, str):
        database = self.get_database_as_json_or_csv()
        file_identifier = self.hash.get_hash_from_file_contents()
        return database, file_identifier

    def get_database_as_json_or_csv(self):
        try:
            if self.is_json:
                data_frame = self.get_database_from_json()
                return data_frame
            else:
                data_frame = self.get_database_from_csv()
                return data_frame
        except ParserWarning:
            quit(F"Format of database in path {self.database_file_path} is not correct")

    def get_database_from_csv(self) -> DataFrame:
        with warnings.catch_warnings():
            warnings.simplefilter("error", category=ParserWarning)
            csv_file = pd.read_csv(self.database_file_path, sep=self.file_format.delimiter,
                                   names=self.file_format.fields, header=None, index_col=False)
            return csv_file

    def get_database_from_json(self):
        try:
            json_file = pd.read_json(self.database_file_path, lines=True)
            return json_file
        except ValueError:
            raise ParserWarning
