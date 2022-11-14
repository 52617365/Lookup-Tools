import os
import shutil
import unittest

from file_glob.file_glob import FileGlob


class TestFileGlobSetup:
    @staticmethod
    def create_files():
        TestFileGlobSetup.__create_recursive_directories()
        TestFileGlobSetup.__create_files_in_recursive_directories()

    @staticmethod
    def __create_files_in_recursive_directories():
        with open("test_dir/test.txt", "w") as test:
            test.write("test")
        with open("test_dir/test_dir_2/test2.txt", "w") as test:
            test.write("test")

    @staticmethod
    def __create_recursive_directories():
        try:
            os.mkdir("test_dir")
            os.mkdir("test_dir/test_dir_2")
        except FileExistsError:
            pass

    @staticmethod
    def clean_files():
        shutil.rmtree("test_dir")


def get_absolute_path(relative_path: str) -> str:
    absolute_path = os.path.join(os.getcwd(), relative_path)
    return absolute_path


class TestFileGlob(unittest.TestCase):
    def setUp(self) -> None:
        self.__setup = TestFileGlobSetup
        self.__setup.create_files()

    def test_recursive_glob(self) -> None:
        file_glob = FileGlob(os.path.dirname(__file__), recursive=True)
        files = file_glob.get_files_from_directories()
        expected_files_found = [get_absolute_path(os.path.join("test_dir", "test.txt")),
                                get_absolute_path(os.path.join("test_dir", "test_dir_2", "test2.txt"))]

        self.assertEqual(expected_files_found, files)

    @classmethod
    def tearDownClass(cls) -> None:
        TestFileGlobSetup.clean_files()


if __name__ == '__main__':
    unittest.main()
