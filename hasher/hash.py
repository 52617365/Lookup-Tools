import hashlib
import os

import pandas as pd
from pandas import DataFrame

from file.csvwriter import CsvWriter


class Hasher:
    def __init__(self, file_data: str, hash_file_path: str = "hashes.txt"):
        self.__file_data = file_data
        self.__hash_file_path = hash_file_path

    def __get_sha256_hash(self) -> str:
        return hashlib.sha256(self.__file_data.encode('utf-8')).hexdigest()

    def write_file_identifier_to_hashes(self):
        # This is not wise to open for each write, maybe pss this writer into the class?
        writer = CsvWriter(self.__hash_file_path, self.__get_sha256_hash())
        writer.write_hash_to_file()


if __name__ == '__main__':
    df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
    hasher = Hasher(df.to_csv())
    hasher.write_file_identifier_to_hashes()
