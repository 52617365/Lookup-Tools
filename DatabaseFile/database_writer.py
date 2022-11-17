import pandas as pd

from hashing.hash import get_sha256_hash_from
from hashing.hash_file_path import get_file_name_for_invalid_hashes_file


class DatabaseWriter:
    def __init__(self, writing_file_path: str, data_to_write: pd.DataFrame, hash_file_path: str):
        self.__path_to_writing_file = writing_file_path
        self.__data_to_write = data_to_write
        self.__hash_file_path = hash_file_path
        self.file_identifier = get_sha256_hash_from(data_to_write)

    def write_as_json(self):
        self.__data_to_write.to_json(self.__path_to_writing_file, orient='records')

    def write_valid_file_hash_to_logs(self):
        with open(self.__hash_file_path, "a") as valid_hashes:
            valid_hashes.write(self.file_identifier + "\n")

    def write_invalid_file_hash_to_logs(self):
        invalid_hashes_file_path = get_file_name_for_invalid_hashes_file(self.__hash_file_path)
        with open(invalid_hashes_file_path, "a") as invalid_hashes:
            invalid_hashes.write(self.file_identifier + "\n")

    def file_is_unique(self) -> bool:
        return not self.__hash_is_already_in_hashes_file()

    def __hash_is_already_in_hashes_file(self):
        with open(self.__hash_file_path, "r") as hashes:
            for line in hashes:
                if line.strip() == self.file_identifier:
                    return True
        return False
