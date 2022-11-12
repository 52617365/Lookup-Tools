import hashlib
import os
from dotenv import load_dotenv

from pandas import DataFrame


class Hasher:
    load_dotenv()

    def __init__(self, file_data: DataFrame, hash_file_path: str = os.getenv("HASH_FILE_PATH")):
        load_dotenv()
        if hash_file_path is None:
            raise Exception("Either set the environment variable HASH_FILE_PATH or pass it as a parameter.")
        self.__hash_file_path = hash_file_path
        self.__file_data = file_data.to_string()

    def __get_sha256_hash(self) -> str:
        return hashlib.sha256(self.__file_data.encode('utf-8')).hexdigest()

    def write_unique_identifier_of_file_to_logs(self):
        # This is not wise to open for each write, maybe pss this writer into the class?
        with open(self.__hash_file_path, "a") as hashes:
            hashes.write(self.__get_sha256_hash() + "\n")
