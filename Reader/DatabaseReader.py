import warnings
from typing import Iterator

import pandas as pd
from pandas.errors import ParserWarning

from Format.FileFormatDeterminer import FileFormat, FileFormatDeterminer
from Format.Input import IDKException


class WeWantToSkipFile(Exception):
    pass


class DatabaseReader:
    def __init__(self, database_file_path: str, specify_format_manually: bool):
        self.database_file_path = database_file_path
        self.file_is_json = self.is_json(database_file_path)
        self.specify_format_manually = specify_format_manually
        self.file_format = self.get_file_format(database_file_path)

    @staticmethod
    def is_json(file_path: str) -> bool:
        return file_path.endswith(".json")

    def get_file_format(self, database_file_path):
        try:
            if not self.file_is_json:
                if self.specify_format_manually:
                    return self.get_file_format_for_csv(database_file_path)
        except StopIteration:
            raise WeWantToSkipFile("The file seems to be junk because it has barely any lines.")
        except IDKException:
            raise WeWantToSkipFile("You did not know the format, skipping.")

    @staticmethod
    def get_file_format_for_csv(database_path: str) -> FileFormat | None:
        file_format = FileFormatDeterminer.determine_file_format(database_path)
        return file_format

    def get_json_or_csv_database_chunks(self):
        if self.file_is_json:
            database_reader = self.get_json_database()
        else:
            database_reader = self.get_csv_database_chunks()
        return database_reader

    def get_json_database(self):
        json_database = pd.read_json(self.database_file_path, chunksize=1000, lines=True)
        return json_database

    def get_csv_database_chunks(self):
        if self.ignored_fields_exist():
            csv_file = self.get_csv_chunks_with_deleted_fields()
        else:
            csv_file = self.get_csv_chunks_with_all_fields()
        return csv_file

    def ignored_fields_exist(self):
        return len(self.file_format.ignored_fields) != 0

    def get_csv_chunks_with_deleted_fields(self):
        fields_to_keep = self.get_fields_we_want_to_keep()

        csv_file = DatabaseReader.get_csv_chunks(database_file_path=self.database_file_path,
                                                 sep=self.file_format.file_delimiter, names=self.file_format.fields,
                                                 use_cols=fields_to_keep, engine="c", header=None)
        return csv_file

    def get_fields_we_want_to_keep(self):
        return list(filter(lambda x: x not in self.file_format.ignored_fields, self.file_format.fields))

    def get_csv_chunks_with_all_fields(self):
        if self.specify_format_manually:
            csv_file_chunks = DatabaseReader.get_csv_chunks(database_file_path=self.database_file_path,
                                                            sep=self.file_format.file_delimiter,
                                                            names=self.file_format.fields,
                                                            engine="c", header=None)
        else:
            csv_file_chunks = DatabaseReader.get_csv_chunks(database_file_path=self.database_file_path,
                                                            engine="python",
                                                            sep='[:;.,\\s+|__]')
        return csv_file_chunks

    @staticmethod
    def get_csv_chunks(database_file_path: str, engine, use_cols=None, sep: str = ',', names=None,
                       header: str | None = "infer"):

        csv_file = pd.read_csv(database_file_path, sep=sep,
                               names=names, header=header,
                               usecols=use_cols, engine=engine, index_col=False, chunksize=1000)
        return csv_file

    @staticmethod
    def terminate_if_csv_database_invalid_format(database_content_chunks: Iterator):
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("error", category=ParserWarning)
                for _ in database_content_chunks:
                    pass

        except ParserWarning:
            quit(F"The file does not have a valid format.")
