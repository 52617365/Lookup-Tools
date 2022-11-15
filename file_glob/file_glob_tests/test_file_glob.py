import os
import shutil
import unittest

from file_glob.file_glob import FileGlob


def get_absolute_path(relative_path: str) -> str:
    return os.path.join(os.getcwd(), relative_path)


def get_tests_base_path():
    base_path = get_absolute_path(os.path.join("file_glob", "file_glob_tests"))
    return base_path


class TestFileGlob(unittest.TestCase):
    def setUp(self) -> None:
        self.__first_file_path = get_absolute_path(os.path.join("file_glob", "file_glob_tests", "dir", "file.txt"))
        self.__second_file_path = get_absolute_path(
            os.path.join("file_glob", "file_glob_tests", "dir", "sub_dir", "file.csv"))
        self.create_startup_files()

    def create_startup_files(self):
        base_path = get_tests_base_path()
        self.create_directories(base_path)
        self.create_files()

    def create_files(self):
        open(self.__first_file_path, "w").close()
        open(self.__second_file_path, "w").close()

    @staticmethod
    def create_directories(base_path):
        try:
            os.makedirs(os.path.join(base_path, "dir"))
        except FileExistsError:
            pass
        try:
            os.makedirs(os.path.join(base_path, "dir", "sub_dir"))
        except FileExistsError:
            pass

    def test_recursive_glob(self) -> None:
        expected_data = [self.__first_file_path, self.__second_file_path]
        actual_data = FileGlob(get_tests_base_path()).get_files_from_directories()
        self.assertEqual(expected_data, actual_data)

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(os.path.join(get_tests_base_path(), "dir"))


if __name__ == '__main__':
    unittest.main()
