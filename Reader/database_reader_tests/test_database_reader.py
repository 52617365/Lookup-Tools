import unittest
from collections import OrderedDict
from unittest.mock import patch

import pandas as pd
from pandas.errors import ParserWarning
from pyfakefs.fake_filesystem_unittest import TestCase

from Connection.DatabaseConnection import DatabaseConnection
from DatabaseWriter.HashWriter import HashWriter
from Format.FileFormatDeterminer import FileFormat
from Format.format_tests.HiddenPrints import HiddenPrints
from Reader.DatabaseReader import DatabaseReader, FileIsJunk


class TestDatabaseReader(TestCase):

    def setUp(self):
        self.setUpPyfakefs()

    @patch('Reader.DatabaseReader.DatabaseReader.get_file_format_for_csv')
    def test_get_valid_comma_delimited_file_as_dataframe(self, mock_get_file_format_for_csv):
        mock_get_file_format_for_csv.return_value = FileFormat(["dir", "test2", "test3"], [], ',')
        testing_file_path = self.create_fake_file("testing_file.csv", "asd1,asd2,asd3")

        example_delimited_file = DatabaseReader(testing_file_path, specify_format_manually=True)
        data = example_delimited_file.get_database_from_csv_with_optional_ignored_fields()
        expected_data = pd.DataFrame({'dir': ["asd1"], 'test2': ["asd2"], 'test3': ["asd3"]})
        self.assertEqual(data.equals(expected_data), True)

    @patch('Reader.DatabaseReader.DatabaseReader.get_file_format_for_csv')
    def test_get_valid_colon_delimited_file_as_dataframe(self, mock_get_file_format_for_csv):
        mock_get_file_format_for_csv.return_value = FileFormat(["dir", "test2", "test3"], [], ':')
        testing_file_path = self.create_fake_file("testing_file.csv", "asd1:asd2:asd3")

        example_delimited_file = DatabaseReader(testing_file_path, specify_format_manually=True)

        data = example_delimited_file.get_database_from_csv_with_optional_ignored_fields()
        expected_data = pd.DataFrame({'dir': ["asd1"], 'test2': ["asd2"], 'test3': ["asd3"]})
        self.assertEqual(data.equals(expected_data), True)

    @patch('Reader.DatabaseReader.DatabaseReader.get_file_format_for_csv')
    def test_get_valid_pipe_delimited_file_as_dataframe(self, mock_get_file_format_for_csv):
        mock_get_file_format_for_csv.return_value = FileFormat(["dir", "test2", "test3"], [], '|')
        testing_file_path = self.create_fake_file("testing_file.csv", "asd1|asd2|asd3")

        example_delimited_file = DatabaseReader(testing_file_path, specify_format_manually=True)
        data = example_delimited_file.get_database_from_csv_with_optional_ignored_fields()
        expected_data = pd.DataFrame({'dir': ["asd1"], 'test2': ["asd2"], 'test3': ["asd3"]})
        self.assertEqual(data.equals(expected_data), True)

    @patch('Reader.DatabaseReader.DatabaseReader.get_file_format_for_csv')
    def test_get_valid_dot_delimited_file_as_dataframe(self, mock_get_file_format_for_csv):
        mock_get_file_format_for_csv.return_value = FileFormat(["dir", "test2", "test3"], [], '.')
        testing_file_path = self.create_fake_file("testing_file.csv", "asd1.asd2.asd3")

        example_delimited_file = DatabaseReader(testing_file_path, specify_format_manually=True)

        data = example_delimited_file.get_database_from_csv_with_optional_ignored_fields()
        expected_data = pd.DataFrame({'dir': ["asd1"], 'test2': ["asd2"], 'test3': ["asd3"]})
        self.assertEqual(data.equals(expected_data), True)

    @patch('Reader.DatabaseReader.DatabaseReader.get_file_format_for_csv')
    def test_get_valid_tab_delimited_file_as_dataframe(self, mock_get_file_format_for_csv):
        mock_get_file_format_for_csv.return_value = FileFormat(["dir", "test2", "test3"], [], '\t')
        testing_file_path = self.create_fake_file("testing_file.csv", "asd1\tasd2\tasd3")

        example_delimited_file = DatabaseReader(testing_file_path, specify_format_manually=True)

        data = example_delimited_file.get_database_from_csv_with_optional_ignored_fields()
        expected_data = pd.DataFrame({'dir': ["asd1"], 'test2': ["asd2"], 'test3': ["asd3"]})
        self.assertEqual(data.equals(expected_data), True)

    @patch('Reader.DatabaseReader.DatabaseReader.get_file_format_for_csv')
    def test_get_csv_invalid_format(self, mock_get_file_format_for_csv):
        with self.assertRaises(ParserWarning):
            mock_get_file_format_for_csv.return_value = FileFormat(fields=["field1", "field2"], ignored_fields=[],
                                                                   file_delimiter=',')
            testing_file_path = self.create_fake_file("invalid_format_file.csv", "value1,value2,value3")

            reader = DatabaseReader(testing_file_path, specify_format_manually=True)

            reader.get_database_from_csv_with_optional_ignored_fields()

    @patch('Reader.DatabaseReader.DatabaseReader.get_file_format_for_csv')
    def test_get_json_invalid_format(self, mock_get_file_format_for_csv):
        mock_get_file_format_for_csv.return_value = FileFormat(["field1", "field2"], [], ',')
        with self.assertRaises(ParserWarning):
            testing_file_path = self.create_fake_file("invalid_format_file.json", "value1,value2,value3")

            reader = DatabaseReader(testing_file_path, specify_format_manually=True)
            reader.get_database_from_json()

    @patch('Reader.DatabaseReader.DatabaseReader.get_file_format_for_csv')
    def test_get_database(self, mock_get_file_format_for_csv):
        mock_get_file_format_for_csv.return_value = FileFormat(["field1", "field2", "field3"], [], ',')

        testing_file_path = self.create_fake_file("testing_file.csv", "asd1,asd2,asd3")

        reader = DatabaseReader(testing_file_path, specify_format_manually=True)
        data_frame, file_identifier = reader.get_database()

        expected_data_frame = pd.DataFrame({'field1': ["asd1"], 'field2': ["asd2"], 'field3': ["asd3"]})
        expected_file_identifier = "bdc56b1c2845a0ff642efb5fc6c6acc35f5cdcc27036deb2493573356a57ce70ecaa72cb71a0b96134afb860519aea1f9ce4b4804478ae3b49f4ce0e4cbc270d"
        self.assertEqual(data_frame.equals(expected_data_frame), True)
        self.assertEqual(expected_file_identifier, file_identifier)

    def test_get_database_as_json(self):
        testing_file_path = self.create_fake_file("testing_file.json",
                                                  '[{"field1": "asd1", "field2": "asd2", "field3": "asd3"}, {"field1": "asd4", "field2": "asd5", "field3": "asd6"}]')

        reader = DatabaseReader(testing_file_path, specify_format_manually=True)

        data_frame, file_identifier = reader.get_database()

        expected_data_frame = pd.DataFrame(
            {'field1': ["asd1", "asd4"], 'field2': ["asd2", "asd5"], 'field3': ["asd3", "asd6"]})
        expected_file_identifier = "c081244bd17fa058e854e199f4c9bfc16990535b204068b5a1c22d53379de00693496beeca231a98179b178be9b70af120f40de6b1eda24a9c5f41775fab49ca"
        self.assertEqual(data_frame.equals(expected_data_frame), True)
        self.assertEqual(expected_file_identifier, file_identifier)

    @patch('Reader.DatabaseReader.DatabaseReader.get_file_format_for_csv')
    def test_get_database_with_ignored_fields(self, mock_get_file_format_for_csv):
        mock_get_file_format_for_csv.return_value = FileFormat(["field1", "field2", "field3"], ["field2"], ',')

        testing_file_path = self.create_fake_file("testing_file.csv", "asd1,asd2,asd3")

        reader = DatabaseReader(testing_file_path, specify_format_manually=True)
        data_frame, file_identifier = reader.get_database()

        expected_data_frame = pd.DataFrame({'field1': ["asd1"], 'field3': ["asd3"]})
        expected_file_identifier = "bdc56b1c2845a0ff642efb5fc6c6acc35f5cdcc27036deb2493573356a57ce70ecaa72cb71a0b96134afb860519aea1f9ce4b4804478ae3b49f4ce0e4cbc270d"
        self.assertEqual(data_frame.equals(expected_data_frame), True)
        self.assertEqual(expected_file_identifier, file_identifier)

    def test_get_file_format_for_csv_raises_file_is_junk(self):
        with self.assertRaises(FileIsJunk):
            with HiddenPrints():
                testing_file_path = self.create_fake_file("testing_file.csv", "asd1,asd2,asd3")

                reader = DatabaseReader(testing_file_path, specify_format_manually=True)
                reader.get_file_format_for_csv("testing_file.csv")

    def test_get_csv_with_all_fields_automatically(self):
        testing_file_path = self.create_fake_file("testing_file.csv", "field1,field2,field3\nasd1,asd2,asd3")

        reader = DatabaseReader(testing_file_path, specify_format_manually=False)
        automatically_determined_csv_file = reader.get_csv_with_all_fields()

        expected_data_frame = pd.DataFrame({'field1': ["asd1"], 'field2': ["asd2"], 'field3': ["asd3"]})
        self.assertEqual(automatically_determined_csv_file.equals(expected_data_frame), True)

    def init_get_database(self, mock_dotenv_values, mongo_server_info):
        self.avoid_exit_if_instance_mongo_instance_does_not_exist(mongo_server_info)
        mock_dotenv_values.return_value = OrderedDict(
            {"CONNECTION_STRING": "test_connection_string", "DATABASE_NAME": "test_database_name",
             "HASHES_COLLECTION_NAME": "test_collection_name",
             "DATABASES_COLLECTION_NAME": "test_databases_collection_name",
             "DATA_COLLECTION_NAME": "test_data_collection_name"})
        hash_collection = DatabaseConnection().hash_collection
        hash_writer = HashWriter(hash_collection)
        return hash_writer

    @staticmethod
    def avoid_exit_if_instance_mongo_instance_does_not_exist(mongo_server_info):
        mongo_server_info.return_value = {"version": "4.4.1"}

    def create_fake_file(self, testing_file_path: str, contents: str):
        self.fs.create_file(testing_file_path, contents=contents)
        return testing_file_path


if __name__ == '__main__':
    unittest.main()
