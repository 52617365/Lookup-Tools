import os


class DatabaseFile:
    def __init__(self, file_path):
        self.__file_name = self.__get_file_without_path_or_extension(file_path)

    @staticmethod
    def __get_file_without_path_or_extension(file_name: str) -> str:
        return os.path.splitext(os.path.basename(file_name))[0]

    def get_file_name(self) -> str:
        return self.__file_name
