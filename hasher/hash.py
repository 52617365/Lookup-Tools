import hashlib

from pandas import DataFrame


class Hasher:
    def __init__(self, file_data: DataFrame):
        self.__file_data = file_data.to_string()

    def get_sha256_hash(self) -> str:
        return hashlib.sha256(self.__file_data.encode('utf-8')).hexdigest()
