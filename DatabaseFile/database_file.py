import os


class DatabaseFile:
    def __init__(self, file_path):
        self.__raise_io_error_if_file_does_not_exist(file_path)
        self.__file_path = file_path
        self.__file_name = self.__get_file_without_path_or_extension(file_path)

    def __raise_io_error_if_file_does_not_exist(self, file_path: str):
        if not self.__is_valid_file(file_path):
            raise IOError(F"File does not exist: {file_path}")

    @staticmethod
    def __get_file_without_path_or_extension(file_name: str) -> str:
        return os.path.splitext(os.path.basename(file_name))[0]

    @staticmethod
    def __is_valid_file(file_path: str) -> bool:
        return os.path.isfile(file_path)

    def get_file_name(self) -> str:
        return self.__file_name

    def get_file_path(self) -> str:
        return self.__file_path
