import warnings

import pandas as pd
from pandas import DataFrame
from pandas.errors import ParserWarning

from Format.FileFormatDeterminer import FileFormat, FileFormatDeterminer
from Reader.Hash import Hash


class FileIsJunk(Exception):
    pass


class DatabaseReader:
    def __init__(self, database_file_path: str, specify_format_manually: bool):
        self.database_file_path = database_file_path
        self.is_json = self.is_json(database_file_path)
        self.specify_format_manually = specify_format_manually
        if not self.is_json:
            if self.specify_format_manually:
                self.file_format = self.get_file_format_for_csv(database_file_path)

    @staticmethod
    def is_json(file_path: str) -> bool:
        return file_path.endswith(".json")

    @staticmethod
    def get_file_format_for_csv(database_path: str) -> FileFormat | None:
        try:
            file_format = FileFormatDeterminer.determine_file_format(database_path)
            return file_format
        except StopIteration:
            raise FileIsJunk

    def get_database(self) -> (pd.DataFrame, str):
        database = self.get_database_as_json_or_csv()
        file_identifier = Hash.get_hash_from_file_contents(self.database_file_path)
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
                csv_file = self.get_csv_without_ignored_fields()
            else:
                csv_file = self.get_csv_with_all_fields()
            return csv_file

    def ignored_fields_exist(self):
        return len(self.file_format.ignored_fields) != 0

    def get_csv_with_all_fields(self):
        if self.specify_format_manually:
            csv_file = DatabaseReader.read_csv(database_file_path=self.database_file_path,
                                               sep=self.file_format.file_delimiter, names=self.file_format.fields,
                                               engine="c", header=None)
        else:
            csv_file = DatabaseReader.read_csv(database_file_path=self.database_file_path, engine="python",
                                               sep='[:;.,\\s+|__]')
        return csv_file

    # TODO: we don't want to do this, instead we want to read the file in chunks.
    def get_csv_without_ignored_fields(self):
        fields_to_keep = self.get_fields_we_want_to_keep()
        csv_file = DatabaseReader.read_csv(database_file_path=self.database_file_path,
                                           sep=self.file_format.file_delimiter, names=self.file_format.fields,
                                           use_cols=fields_to_keep, engine="c", header=None)
        return csv_file

    def get_fields_we_want_to_keep(self):
        return list(filter(lambda x: x not in self.file_format.ignored_fields, self.file_format.fields))

    @staticmethod
    def read_csv(database_file_path: str, engine, use_cols=None, sep: str = ',', names=None,
                 header: str | None = "infer"):
        csv_file = pd.read_csv(database_file_path, sep=sep,
                               names=names, header=header, index_col=False,
                               usecols=use_cols, engine=engine)
        return csv_file

    # TODO: we don't want to do this, instead we want to read the file in chunks.
    def get_database_from_json(self):
        try:
            json_file = pd.read_json(self.database_file_path)
            return json_file
        except ValueError:
            raise ParserWarning
