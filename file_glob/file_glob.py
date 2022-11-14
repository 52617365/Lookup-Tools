import glob
import os


def get_current_directory() -> str:
    return os.path.dirname(__file__)


class FileGlob:
    def __init__(self, path=get_current_directory(), recursive=False):
        self.path = path
        self.recursive = recursive

    def get_files_from_directories(self):
        all_file_paths_from_directories = glob.glob(F'{self.path}/**/*', recursive=True)
        files = self.__get_files_with_supported_extension(all_file_paths_from_directories)
        return files

    def __get_files_with_supported_extension(self, all_file_paths: list) -> list:
        files_with_supported_extension = []
        for file in all_file_paths:
            if self.__has_supported_extension(file):
                files_with_supported_extension.append(file)
        return files_with_supported_extension

    @staticmethod
    def __has_supported_extension(file_path: str) -> bool:
        return file_path.endswith('.txt') or file_path.endswith('.csv')


if __name__ == '__main__':
    file_glob = FileGlob(recursive=False)
    files = file_glob.get_files_from_directories()
    print(files)
