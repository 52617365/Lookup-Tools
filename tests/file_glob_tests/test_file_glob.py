import os
import pathlib
import shutil
import unittest

from file_glob.file_glob import FileGlob


# TODO: this setup is fucked. Fix it on 15.11.2022
class TestFileGlobSetup:
    @staticmethod
    def create_files():
        TestFileGlobSetup.__create_recursive_directories()
        TestFileGlobSetup.__create_files_in_recursive_directories()

    @staticmethod
    def __create_files_in_recursive_directories():
        open(get_absolute_path("test/test.txt"), "w").close()
        open(get_absolute_path("test/test2/test2.txt"), "w").close()

    @staticmethod
    def __create_recursive_directories():
        try:
            os.mkdir("test")
            os.mkdir(os.path.join("test", "test2"))
        except FileExistsError:
            pass

    @staticmethod
    def clean_files():
        shutil.rmtree("test")


def get_absolute_path(relative_path: str) -> str:
    absolute_path = os.path.join(os.getcwd(), relative_path)
    return absolute_path


def get_current_path():
    return pathlib.Path(__file__).parent.resolve()


class TestFileGlob(unittest.TestCase):
    def setUp(self) -> None:
        TestFileGlobSetup().create_files()

    def test_recursive_glob(self) -> None:
        file_glob = FileGlob(path=get_current_path())
        files = file_glob.get_files_from_directories()
        expected_files_found = [get_absolute_path(os.path.join("file_glob_tests", "test", "test.txt")),
                                get_absolute_path(os.path.join("file_glob_tests", "test", "test2", "test2.txt"))]

        self.assertEqual(expected_files_found, files)

    @classmethod
    def tearDownClass(cls) -> None:
        TestFileGlobSetup.clean_files()


if __name__ == '__main__':
    unittest.main()
