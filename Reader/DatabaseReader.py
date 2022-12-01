import warnings

import pandas as pd
from pandas import DataFrame
from pandas.errors import ParserWarning

from Format.FileFormatDeterminer import FileFormat, FileFormatDeterminer
from Reader.Hash import Hash


class FileIsJunk(Exception):
    pass


class DatabaseReader:
    def __init__(self, database_file_path: str):
        self.database_file_path = database_file_path
        self.is_json = self.is_json(database_file_path)
        if not self.is_json:
            self.file_format = self.get_file_format_for_csv(database_file_path)

        self.hash = Hash(self.database_file_path)

    @staticmethod
    def is_json(file_path: str) -> bool:
        return file_path.endswith(".json")

    @staticmethod
    def get_file_format_for_csv(database_path: str) -> FileFormat | None:
        try:
            determiner = FileFormatDeterminer(database_path, 5)
            file_format = determiner.determine_file_format()
            return file_format
        except StopIteration:
            raise FileIsJunk

    def get_database(self) -> (pd.DataFrame, str):
        database = self.get_database_as_json_or_csv()
        file_identifier = self.hash.get_hash_from_file_contents()
        return database, file_identifier

    def get_database_as_json_or_csv(self):
        try:
            if self.is_json:
                data_frame = self.get_database_from_json()
            else:
                data_frame = self.get_database_from_csv_with_optional_ignored_fields()
            return data_frame
        except ParserWarning:
            quit(F"Format of database in path {self.database_file_path} is not correct")

    def get_database_from_csv_with_optional_ignored_fields(self) -> DataFrame:
        with warnings.catch_warnings():
            warnings.simplefilter("error", category=ParserWarning)
            if self.ignored_fields_exist():
                csv_file = self.get_csv_without_without_ignored_fields()
            else:
                csv_file = self.get_csv_with_all_fields()
            return csv_file

    def ignored_fields_exist(self):
        return len(self.file_format.ignored_fields) != 0

    def get_csv_with_all_fields(self):
        csv_file = pd.read_csv(self.database_file_path, sep=self.file_format.file_delimiter,
                               names=self.file_format.fields, header=None, index_col=False)
        # Deleting NaN values if they're present to save disk space.
        csv_file = csv_file.dropna(axis=1)
        return csv_file

    def get_csv_without_without_ignored_fields(self):
        fields_to_keep = self.get_fields_we_want_to_keep()
        csv_file = pd.read_csv(self.database_file_path, sep=self.file_format.file_delimiter,
                               names=self.file_format.fields, header=None, index_col=False,
                               usecols=fields_to_keep)
        # Deleting NaN values if they're present to save disk space.
        csv_file = csv_file.dropna(axis=1)
        return csv_file

    def get_fields_we_want_to_keep(self):
        return list(filter(lambda x: x not in self.file_format.ignored_fields, self.file_format.fields))

    def get_database_from_json(self):
        try:
            json_file = pd.read_json(self.database_file_path)
            return json_file
        except ValueError:
            raise ParserWarning
