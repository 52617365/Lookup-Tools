import hashlib
import os

from dotenv import load_dotenv
from pandas import DataFrame


class HashFilePath:
    def __init__(self, hash_file_path: str):
        load_dotenv()
        self.__hash_file_path_environment_variable = os.getenv("HASH_FILE_PATH")
        self.__user_specified_hash_file_path = hash_file_path

    def get(self):
        if self.user_wants_to_use_user_specified_hash_file_path():
            return self.__get_user_specified_hash_file_path()
        if self.user_wants_to_use_environment_variable():
            return self.__get_environment_variable()
        else:
            quit("No hash file path specified.")

    def user_wants_to_use_environment_variable(self) -> bool:
        return self.__variable_is_set() and self.__user_specified_hash_file_path is None

    def __variable_is_set(self) -> bool:
        return self.__hash_file_path_environment_variable is not None

    def user_wants_to_use_user_specified_hash_file_path(self) -> bool:
        return self.__user_specified_hash_file_path is not None

    def __get_environment_variable(self) -> str:
        return self.__hash_file_path_environment_variable

    def __get_user_specified_hash_file_path(self) -> str:
        return self.__user_specified_hash_file_path


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
