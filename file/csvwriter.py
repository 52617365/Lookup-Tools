import sys

import pandas as pd
from pandas import DataFrame

from hasher.hash import Hasher


class CsvWriter:
    def __init__(self, writing_file_path: str, data_to_write: pd.DataFrame):
        self.__path_to_writing_file = writing_file_path
        self.__data_to_write = data_to_write

    def write_as_json(self):
        self.__data_to_write.to_json(self.__path_to_writing_file, orient='records')
        self.__write_hash_to_file()

    def write_as_csv(self):
        self.__data_to_write.to_csv(self.__path_to_writing_file, index=False)
        self.__write_hash_to_file()

    def __write_hash_to_file(self):
        if isinstance(self.__data_to_write, DataFrame):
            hasher = Hasher(self.__data_to_write)
            hasher.write_unique_identifier_of_file_to_logs()
        else:
            print("This function can only be called with Dataframes.")
            sys.exit(1)
