import hashlib

from pandas import DataFrame

from hasher.hash_file_path import HashFilePath


class Hasher:
    def __init__(self, file_data: DataFrame, hash_file_path: str = "file_hashes.txt"):
        self.__hash_file_path = HashFilePath(hash_file_path).get()
        self.__file_data = file_data.to_string()

    def __get_sha256_hash(self) -> str:
        return hashlib.sha256(self.__file_data.encode('utf-8')).hexdigest()

    def write_unique_identifier_of_file_to_logs(self):
        # This is not wise to open for each write, maybe pss this writer into the class?
        with open(self.__hash_file_path, "a") as hashes:
            hashes.write(self.__get_sha256_hash() + "\n")

    def get_hash_file_path(self):
        return self.__hash_file_path
