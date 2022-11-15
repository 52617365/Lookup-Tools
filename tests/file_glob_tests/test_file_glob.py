import os
import shutil
import unittest

from file_glob.file_glob import FileGlob


def get_current_path():
    return os.getcwd()


class TestFileGlob(unittest.TestCase):
    def setUp(self) -> None:
        self.create_startup_files()

    @staticmethod
    def create_startup_files():
        os.makedirs("dir")
        os.makedirs(os.path.join("dir", "sub_dir"))
        open("dir/file.txt", "w").close()
        open(os.path.join("dir", "sub_dir", "file.csv"), "w").close()

    def test_recursive_glob(self) -> None:
        expected_data = [os.path.join(get_current_path(), "dir", "file.txt"),
                         os.path.join(get_current_path(), "dir", "sub_dir", "file.csv")]
        actual_data = FileGlob(os.getcwd()).get_files_from_directories()
        self.assertEqual(expected_data, actual_data)

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree("dir")


if __name__ == '__main__':
    unittest.main()
