import warnings
from typing import Iterator

import pandas as pd
from pandas.errors import ParserWarning, ParserError

from Format.FileFormatDeterminer import FileFormat, FileFormatDeterminer
from Format.Input import IDKException


class WeWantToSkipFile(Exception):
    pass


class DatabaseReader:
    def __init__(self, database_file_path: str, specify_format_manually: bool, skip_invalid_lines: bool):
        self.database_file_path = database_file_path
        self.file_is_json = self.is_json(database_file_path)
        self.specify_format_manually = specify_format_manually
        self.file_format = self.get_file_format(database_file_path)
        self.skip_invalid_lines = skip_invalid_lines

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

    def get_json_or_csv_database_chunk_iterator(self):
        if self.file_is_json:
            database_reader = self.get_json_database_chunk_iterator()
        else:
            database_reader = self.get_csv_database_chunk_iterator()
        return database_reader

    def get_json_database_chunk_iterator(self):
        with pd.read_json(self.database_file_path, chunksize=1000, lines=True) as chunks:
            for chunk in chunks:
                yield chunk

    def get_csv_database_chunk_iterator(self):
        if self.ignored_fields_exist():
            csv_file = self.get_csv_chunk_iterator_with_deleted_fields()
        else:
            csv_file = self.get_csv_chunk_iterator_with_all_fields()
        return csv_file

    def ignored_fields_exist(self):
        return len(self.file_format.ignored_fields) != 0

    def get_csv_chunk_iterator_with_deleted_fields(self):
        fields_to_keep = self.get_fields_we_want_to_keep()

        csv_file = self.get_csv_chunk_iterator(database_file_path=self.database_file_path,
                                               sep=self.file_format.file_delimiter,
                                               names=self.file_format.fields,
                                               use_cols=fields_to_keep, engine="c", header=None)
        return csv_file

    def get_fields_we_want_to_keep(self):
        return list(filter(lambda x: x not in self.file_format.ignored_fields, self.file_format.fields))

    def get_csv_chunk_iterator_with_all_fields(self):
        if self.specify_format_manually:
            csv_file_chunks = self.get_csv_chunk_iterator(database_file_path=self.database_file_path,
                                                          sep=self.file_format.file_delimiter,
                                                          names=self.file_format.fields,
                                                          engine="c", header=None)
        else:
            csv_file_chunks = self.get_csv_chunk_iterator(database_file_path=self.database_file_path,
                                                          engine="python",
                                                          sep='[:;.,\\s+|__]')
        return csv_file_chunks

    def get_csv_chunk_iterator(self, database_file_path: str, engine, use_cols=None, sep: str = ',',
                               names=None,
                               header: str | None = "infer"):

        if self.skip_invalid_lines:
            with pd.read_csv(database_file_path, sep=sep,
                             names=names, header=header,
                             usecols=use_cols, engine=engine, chunksize=100000, on_bad_lines='skip'
                             ) as chunks:
                for chunk in chunks:
                    yield chunk
        else:
            with pd.read_csv(database_file_path, sep=sep,
                             names=names, header=header,
                             usecols=use_cols, engine=engine, chunksize=100000, index_col=False
                             ) as chunks:
                for chunk in chunks:
                    yield chunk

    @staticmethod
    def terminate_if_csv_database_invalid_format(database_content_chunks: Iterator):
        print("Validating the format of the database...")
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("error", category=ParserWarning)
                while True:
                    try:
                        next(database_content_chunks)
                    except StopIteration:
                        break
        except ParserWarning:
            quit(F"The file does not have a valid format.")
        except ParserError:
            quit(F"The file does not have a valid format.")
