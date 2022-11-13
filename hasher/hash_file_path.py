import os

from dotenv import load_dotenv


class HashFilePath:
    def __init__(self, hash_file_path: str = None):
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

    def user_wants_to_use_user_specified_hash_file_path(self) -> bool:
        return self.__user_specified_hash_file_path is not None

    def __get_user_specified_hash_file_path(self) -> str:
        return self.__user_specified_hash_file_path

    def user_wants_to_use_environment_variable(self) -> bool:
        return self.__variable_is_set() and self.__user_specified_hash_file_path is None

    def __variable_is_set(self) -> bool:
        return self.__hash_file_path_environment_variable is not None

    def __get_environment_variable(self) -> str:
        self.__terminate_if_env_value_invalid()
        return self.__hash_file_path_environment_variable

    def __terminate_if_env_value_invalid(self):
        if self.__hash_file_path_environment_variable == "":
            quit("Environment variable HASH_FILE_PATH is set but empty.")
