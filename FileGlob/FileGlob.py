import glob
import os
from os import path
from pathlib import Path


class FileGlob:
    def __init__(self, path_to_glob: Path):
        self.path = path_to_glob

    def get_files_from_directories(self):
        path_to_glob = path.join(os.getcwd(), self.path, "**", "*")
        all_file_paths_from_directories = glob.glob(path_to_glob, recursive=True)
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
        return file_path.endswith('.txt') or file_path.endswith('.csv') or file_path.endswith('.json')
