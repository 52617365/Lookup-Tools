import os
import unittest

import pandas as pd

from DatabaseIO.DatabaseReader import DatabaseReader


class DatabaseFileReaderSetup:
    def __init__(self):
        DatabaseFileReaderSetup.create_files(self)

    def create_files(self):
        self.create_testing_file()
        self.create_invalid_file_path()

    @staticmethod
    def create_testing_file():
        data = "dir,test2,test3\nasd1,asd2,asd3"

        file_handle = open('testing_file.csv', "w")
        file_handle.write(data)
        file_handle.close()

    @staticmethod
    def create_invalid_file_path():
        invalid_data = "dir,test2,test3\nasd1,asd2,asd3,asd4"
        # write to DatabaseIO
        file_handle = open('invalid_format_file.csv', "w")
        file_handle.write(invalid_data)
        file_handle.close()

    @staticmethod
    def clean_files():
        os.remove('testing_file.csv')
        os.remove('invalid_format_file.csv')


def get_platform_independent_relative_path(relative_path_to_file: str) -> str:
    dir_name = os.path.dirname(__file__)
    filename = os.path.join(dir_name, relative_path_to_file)
    return filename


class TestDatabaseReader(unittest.TestCase):
    def setUp(self):
        DatabaseFileReaderSetup()

    def test_get_valid_file_as_dataframe(self):
        testing_file_path = "testing_file.csv"

        example_delimited_file = DatabaseReader(testing_file_path)
        data = example_delimited_file.get_database_as_dataframe()
        expected_data = pd.DataFrame({'dir': ["asd1"], 'test2': ["asd2"], 'test3': ["asd3"]})
        self.assertEqual(data.equals(expected_data), True)

    def test_get_dataframe_file_with_file_that_has_invalid_format(self):
        with self.assertRaises(Exception):
            testing_file_path = 'invalid_format_file.csv'
            f = DatabaseReader(testing_file_path)
            f.get_database_as_dataframe()

    @classmethod
    def tearDownClass(cls) -> None:
        DatabaseFileReaderSetup.clean_files()


if __name__ == '__main__':
    unittest.main()
