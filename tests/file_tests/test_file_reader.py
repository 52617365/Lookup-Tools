import os
import unittest

import pandas as pd

from file.filereader import FileReader


def get_relative_path_to_file(relative_path_to_file: str) -> str:
    dir_name = os.path.dirname(__file__)
    relative_path = os.path.join(dir_name, relative_path_to_file)
    return relative_path


class TestFileReader(unittest.TestCase):
    def test_get_valid_file_as_dataframe(self):
        testing_file_path = get_relative_path_to_file('files/testing_file.txt')

        example_delimited_file = FileReader(testing_file_path)
        data = example_delimited_file.get_file_as_dataframe()
        expected_data = pd.DataFrame({'test': ["asd1"], 'test2': ["asd2"], 'test3': ["asd3"]})
        self.assertEqual(data.equals(expected_data), True)

    def test_get_file_as_dataframe_with_file_that_does_not_exist(self):
        with self.assertRaises(IOError):
            FileReader("file_that_does_not_exist.csv")

    def test_get_dataframe_file_with_file_that_is_invalid(self):
        with self.assertRaises(Exception):
            testing_file_path = get_relative_path_to_file('files/invalid_format_file.csv')

            f = FileReader(testing_file_path)
            f.get_file_as_dataframe()


if __name__ == '__main__':
    unittest.main()
