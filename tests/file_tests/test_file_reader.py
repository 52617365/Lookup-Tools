import os
import unittest

import pandas as pd

from file.filereader import FileReader


class TestFileReader(unittest.TestCase):
    def test_get_valid_file_as_dataframe(self):
        current_working_directory = os.getcwd()
        testing_file_path = F"{current_working_directory}\\file_tests\\files\\testing_file.txt"
        print(testing_file_path)

        example_delimited_file = FileReader(testing_file_path)
        data = example_delimited_file.get_file_as_dataframe()
        expected_data = pd.DataFrame({'test': ["asd1"], 'test2': ["asd2"], 'test3': ["asd3"]})
        self.assertEqual(data.equals(expected_data), True)

    def test_get_file_as_dataframe_with_file_that_does_not_exist(self):
        with self.assertRaises(IOError):
            FileReader("file_that_does_not_exist.csv")

    def test_get_dataframe_file_with_file_that_is_invalid(self):
        with self.assertRaises(Exception):
            f = FileReader("files/invalid_format_file.csv")
            file = f.get_file_as_dataframe()


if __name__ == '__main__':
    unittest.main()
