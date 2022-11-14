import hashlib

from pandas import DataFrame

from hasher.hash_file_path import HashFilePath
from hasher.hash_file_path import get_file_name_for_invalid_hashes_file


class Hasher:
    def __init__(self, file_data: DataFrame, hash_file_path: str = None):
        self.__file_data = file_data.to_string()
        self.__hash_file_path = HashFilePath(hash_file_path).get()

    def write_valid_file_hash_to_logs(self):
        # This is not wise to open for each write, maybe pass this writer into the class?
        with open(self.__hash_file_path, "a") as valid_hashes:
            valid_hashes.write(self.__get_sha256_hash() + "\n")

    def write_invalid_file_hash_to_logs(self):
        invalid_hashes_file_path = get_file_name_for_invalid_hashes_file(self.__hash_file_path)
        with open(invalid_hashes_file_path, "a") as invalid_hashes:
            invalid_hashes.write(self.__get_sha256_hash() + "\n")

    def file_is_unique(self) -> bool:
        return not self.__hash_is_already_in_hashes_file()

    def __hash_is_already_in_hashes_file(self):
        hash_to_check_for = self.__get_sha256_hash()
        with open(self.__hash_file_path, "r") as hashes:
            for line in hashes:
                if line.strip() == hash_to_check_for:
                    return True
        return False

    def __get_sha256_hash(self) -> str:
        return hashlib.sha256(self.__file_data.encode('utf-8')).hexdigest()

    def get_hash_file_path(self):
        return self.__hash_file_path
