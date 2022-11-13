import os

from dotenv import load_dotenv


class HashFilePath:
    def __init__(self, hash_file_path: str = None):
        load_dotenv()
        self.__hash_file_path_environment_variable = os.getenv("HASH_FILE_PATH")
        self.__user_specified_hash_file_path = hash_file_path

    def get(self):
        if self.__user_wants_to_use_user_specified_hash_file_path():
            return self.__get_user_specified_hash_file_path()
        if self.__user_wants_to_use_environment_variable():
            return self.__get_environment_variable()
        else:
            quit("No hash file path specified.")

    def __user_wants_to_use_user_specified_hash_file_path(self) -> bool:
        return self.__user_specified_hash_file_path is not None

    def __get_user_specified_hash_file_path(self) -> str:
        if self.__path_is_valid(self.__user_specified_hash_file_path):
            return self.__user_specified_hash_file_path
        else:
            quit("User specified hash file path is invalid.")

    def __user_wants_to_use_environment_variable(self) -> bool:
        return self.__variable_is_set() and self.__user_specified_hash_file_path is None

    def __variable_is_set(self) -> bool:
        return self.__hash_file_path_environment_variable is not None

    def __get_environment_variable(self) -> str:
        self.__terminate_if_env_value_path_invalid()
        return self.__hash_file_path_environment_variable

    def __terminate_if_env_value_path_invalid(self):
        if not self.__path_is_valid(self.__hash_file_path_environment_variable):
            quit("Environment variable HASH_FILE_PATH is set but invalid.")

    @staticmethod
    def __path_is_valid(file_path) -> bool:
        if HashFilePath.__path_exists(file_path) and file_path != "":
            return True
        return False

    @staticmethod
    def __path_exists(file_path):
        try:
            HashFilePath.__get_handle_to_file(file_path)
            return True
        except OSError:
            return False

    @staticmethod
    def __get_handle_to_file(file_path):
        handler_to_file = None
        try:
            handler_to_file = HashFilePath.__open_or_create_file(file_path)
        except OSError as e:
            raise e
        finally:
            if handler_to_file is not None:
                handler_to_file.close()

    @staticmethod
    def __open_or_create_file(file_path):
        handler_to_file = open(file_path, "a")
        return handler_to_file
