import os.path
import unittest
from pathlib import Path

from pyfakefs.fake_filesystem_unittest import TestCase

from FileGlob.FileGlob import FileGlob


class TestFileGlob(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    def test_recursive_glob(self) -> None:
        self.create_glob_files()
        current_path = Path(__file__).parent.absolute()
        actual_data = FileGlob(current_path).get_files_from_directories()
        expected_data = [os.path.join(current_path, 'main_dir', 'test.txt'),
                         os.path.join(current_path, 'main_dir', 'sub_dir', 'test2.txt'),
                         os.path.join(current_path, 'main_dir', 'sub_dir', 'sub_sub_dir', 'test3.csv')]
        self.assertEqual(expected_data, actual_data)

    def create_glob_files(self):
        self.create_directories()
        self.create_files()

    def create_directories(self):
        self.fs.create_dir(os.path.join(Path(__file__).parent.absolute(), "main_dir"))
        self.fs.create_dir(os.path.join(Path(__file__).parent.absolute(), "main_dir", "sub_dir"))
        self.fs.create_dir(os.path.join(Path(__file__).parent.absolute(), "main_dir", "sub_dir", "sub_sub_dir"))

    def create_files(self):
        self.fs.create_file(os.path.join(Path(__file__).parent.absolute(), "main_dir", "test.txt"))
        self.fs.create_file(
            os.path.join(Path(__file__).parent.absolute(), "main_dir", "sub_dir", "test2.txt"))
        self.fs.create_file(
            os.path.join(Path(__file__).parent.absolute(), "main_dir", "sub_dir", "sub_sub_dir", "test3.csv"))


if __name__ == '__main__':
    unittest.main()
