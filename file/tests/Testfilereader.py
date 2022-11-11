import unittest

import pandas as pd

from file.filereader import FileReader


class MyTestCase(unittest.TestCase):
    def test_get_valid_file_as_dataframe(self):
        example_delimited_file = FileReader("testing_file.txt")
        data = example_delimited_file.get_file_as_dataframe()
        expected_data = pd.DataFrame({'test': ["asd1"], 'test2': ["asd2"], 'test3': ["asd3"]})
        self.assertEqual(data.equals(expected_data), True)

    def test_get_file_as_dataframe_with_file_that_does_not_exist(self):
        with self.assertRaises(IOError):
            FileReader("file_that_does_not_exist.csv")

    def test_get_dataframe_file_with_file_that_is_invalid(self):
        # TODO: make this pass.
        with self.assertRaises(Exception):
            f = FileReader("invalid_format_file.csv")
            file = f.get_file_as_dataframe()


if __name__ == '__main__':
    unittest.main()
