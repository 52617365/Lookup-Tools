import hashlib

from pandas import DataFrame

from hasher.hash_file_path import HashFilePath


class Hasher:
    def __init__(self, file_data: DataFrame, hash_file_path: str = None):
        self.__file_data = file_data.to_string()
        self.__hash_file_path = HashFilePath(hash_file_path).get()

    def write_unique_identifier_of_file_to_logs(self):
        # This is not wise to open for each write, maybe pss this writer into the class?
        with open(self.__hash_file_path, "a") as hashes:
            hashes.write(self.__get_sha256_hash() + "\n")

    def __get_sha256_hash(self) -> str:
        return hashlib.sha256(self.__file_data.encode('utf-8')).hexdigest()

    def is_file_unique(self) -> bool:
        return not self.__is_hash_already_in_hashes_file()

    def __is_hash_already_in_hashes_file(self):
        with open(self.__hash_file_path, "r") as hashes:
            for line in hashes:
                if line.strip() == self.__get_sha256_hash():
                    return True
        return False

    def get_hash_file_path(self):
        return self.__hash_file_path
