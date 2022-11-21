import os
import unittest
from collections import OrderedDict
from unittest.mock import patch

import pandas as pd
from pyfakefs.fake_filesystem_unittest import TestCase

from DatabaseIO.DatabaseReader import DatabaseReader
from DatabaseIO.HashWriter import HashWriter


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


class TestDatabaseReader(TestCase):

    def setUp(self):
        self.setUpPyfakefs()

    def test_get_valid_file_as_dataframe(self):
        testing_file_path = self.create_fake_file("testing_file.csv", "dir,test2,test3\nasd1,asd2,asd3")

        example_delimited_file = DatabaseReader(testing_file_path, None)
        data = example_delimited_file.get_database_as_dataframe()
        expected_data = pd.DataFrame({'dir': ["asd1"], 'test2': ["asd2"], 'test3': ["asd3"]})
        self.assertEqual(data.equals(expected_data), True)

    def test_get_dataframe_file_with_file_that_has_invalid_format(self):
        with self.assertRaises(Exception):
            testing_file_path = self.create_fake_file("invalid_format_file.csv", "field1,field2\nvalue1,value2,value3")
            f = DatabaseReader(testing_file_path, None)
            f.get_database_as_dataframe()

    @patch('DatabaseIO.HashWriter.dotenv_values')
    def test_get_database(self, mock_dotenv_values):
        testing_file_path = self.create_fake_file("testing_file.csv", "field1,field2,field3\nasd1,asd2,asd3")

        mock_dotenv_values.return_value = OrderedDict(
            {"CONNECTION_STRING": "test_connection_string", "DATABASE_NAME": "test_database_name",
             "COLLECTION_NAME": "test_collection_name"})

        hash_writer = HashWriter()
        reader = DatabaseReader(testing_file_path, hash_writer)
        csv_file, file_identifier = reader.get_database()

        expected_csv_file = pd.DataFrame({'field1': ["asd1"], 'field2': ["asd2"], 'field3': ["asd3"]})
        expected_file_identifier = "0a85dea3cfe57ca01ab859e954acde77ae8caf899647e4d1f9c01ed55995a03fc7445ada4ac67567390082532d5996876bed744677a502f415bfce26ee3847a0"
        self.assertEqual(csv_file.equals(expected_csv_file), True)
        self.assertEqual(expected_file_identifier, file_identifier)

    def create_fake_file(self, testing_file_path: str, contents: str):
        self.fs.create_file(testing_file_path, contents=contents)
        return testing_file_path


if __name__ == '__main__':
    unittest.main()
