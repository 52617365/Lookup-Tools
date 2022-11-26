import unittest
from collections import OrderedDict
from unittest.mock import patch

import pandas as pd
from pyfakefs.fake_filesystem_unittest import TestCase

from Connection.DatabaseConnection import DatabaseConnection
from DatabaseWriter.HashWriter import HashWriter
from Reader.DatabaseReader import DatabaseReader


class TestDatabaseReader(TestCase):

    def setUp(self):
        self.setUpPyfakefs()

    def test_get_valid_comma_delimited_file_as_dataframe(self):
        testing_file_path = self.create_fake_file("testing_file.csv", "dir,test2,test3\nasd1,asd2,asd3")

        example_delimited_file = DatabaseReader(testing_file_path, None)
        data = example_delimited_file.get_database_as_dataframe()
        expected_data = pd.DataFrame({'dir': ["asd1"], 'test2': ["asd2"], 'test3': ["asd3"]})
        self.assertEqual(data.equals(expected_data), True)

    def test_get_valid_colon_delimited_file_as_dataframe(self):
        testing_file_path = self.create_fake_file("testing_file.csv", "dir:test2:test3\nasd1:asd2:asd3")

        example_delimited_file = DatabaseReader(testing_file_path, None)
        data = example_delimited_file.get_database_as_dataframe()
        expected_data = pd.DataFrame({'dir': ["asd1"], 'test2': ["asd2"], 'test3': ["asd3"]})
        self.assertEqual(data.equals(expected_data), True)

    def test_get_dataframe_file_with_file_that_has_invalid_format(self):
        with self.assertRaises(Exception):
            testing_file_path = self.create_fake_file("invalid_format_file.csv", "field1,field2\nvalue1,value2,value3")
            f = DatabaseReader(testing_file_path, None)
            f.get_database_as_dataframe()

    @patch('Connection.DatabaseConnection.pymongo.MongoClient.server_info')
    @patch('Connection.DatabaseConnection.dotenv_values')
    def test_get_database(self, mock_dotenv_values, mongo_server_info):
        testing_file_path = self.create_fake_file("testing_file.csv", "field1,field2,field3\nasd1,asd2,asd3")

        self.avoid_exit_if_instance_mongo_instance_does_not_exist(mongo_server_info)

        mock_dotenv_values.return_value = OrderedDict(
            {"CONNECTION_STRING": "test_connection_string", "DATABASE_NAME": "test_database_name",
             "HASHES_COLLECTION_NAME": "test_collection_name",
             "DATABASES_COLLECTION_NAME": "test_databases_collection_name",
             "DATA_COLLECTION_NAME": "test_data_collection_name"})

        hash_collection = DatabaseConnection().hash_collection
        hash_writer = HashWriter(hash_collection)

        reader = DatabaseReader(testing_file_path, hash_writer)
        csv_file, file_identifier = reader.get_database()

        expected_csv_file = pd.DataFrame({'field1': ["asd1"], 'field2': ["asd2"], 'field3': ["asd3"]})
        expected_file_identifier = "0a85dea3cfe57ca01ab859e954acde77ae8caf899647e4d1f9c01ed55995a03fc7445ada4ac67567390082532d5996876bed744677a502f415bfce26ee3847a0"
        self.assertEqual(csv_file.equals(expected_csv_file), True)
        self.assertEqual(expected_file_identifier, file_identifier)

    @staticmethod
    def avoid_exit_if_instance_mongo_instance_does_not_exist(mongo_server_info):
        mongo_server_info.return_value = {"version": "4.4.1"}

    def create_fake_file(self, testing_file_path: str, contents: str):
        self.fs.create_file(testing_file_path, contents=contents)
        return testing_file_path


if __name__ == '__main__':
    unittest.main()
