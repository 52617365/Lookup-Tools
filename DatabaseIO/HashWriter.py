import hashlib

import pandas as pd
from pandas import DataFrame

from hashing.HashFilePath import get_file_name_for_invalid_hashes_file


class HashWriter:
    def __init__(self, data_to_write: pd.DataFrame, hash_file_path: str):
        self.__hash_file_path = hash_file_path
        self.file_identifier = self.get_sha256_hash_from(data_to_write)

    @staticmethod
    def get_sha256_hash_from(data_to_write: DataFrame) -> str:
        file_data = data_to_write.to_string()
        return hashlib.sha256(file_data.encode('utf-8')).hexdigest()

    def write_valid_file_hash_to_logs(self):
        with open(self.__hash_file_path, "a") as valid_hashes:
            valid_hashes.write(self.file_identifier + "\n")

    def write_invalid_file_hash_to_logs(self):
        invalid_hashes_file_path = get_file_name_for_invalid_hashes_file(self.__hash_file_path)
        with open(invalid_hashes_file_path, "a") as invalid_hashes:
            invalid_hashes.write(self.file_identifier + "\n")

    def file_is_unique(self) -> bool:
        return not self.__hash_is_already_in_hashes_file()

    # TODO: could load the hashes file once into a list then append to it instead of looking at hashes file each time.
    def __hash_is_already_in_hashes_file(self):
        with open(self.__hash_file_path, "r") as hashes:
            for line in hashes:
                if line.strip() == self.file_identifier:
                    return True
        return False
