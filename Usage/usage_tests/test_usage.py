import os
import unittest
from types import SimpleNamespace
from unittest.mock import patch

import mongomock
import pandas as pd
from pyfakefs.fake_filesystem_unittest import TestCase

from Format.FileFormatDeterminer import FileFormat
from Usage.Usage import Usage


class TestUsage(TestCase):
    def setUp(self) -> None:
        self.setUpPyfakefs()

    @patch('Usage.UserArguments.argparse.ArgumentParser.parse_args')
    def test_usage_constructor(self, command_line_arguments_mock):
        command_line_arguments_mock.return_value = SimpleNamespace(input='test_input.txt',
                                                                   additional='test_additional.txt',
                                                                   glob=False)

        self.create_mocks()

        hash_collection, data_collection, database_collection = self.create_mock_collections()
        instance = Usage(hash_collection, data_collection, database_collection)

        self.assertTrue(instance.additional_information.equals(
            pd.DataFrame({"database": ["exampledata"], "entries": [22222], "dumped": ["2022-02-02"]})))
        self.assertEqual(instance.hash_writer.mongo_hash_collection, hash_collection)

    @patch('Usage.UserArguments.argparse.ArgumentParser.parse_args')
    def test_get_database_paths_if_glob_false(self, command_line_arguments_mock):
        command_line_arguments_mock.return_value = SimpleNamespace(input='test_input.txt',
                                                                   additional='test_additional.txt',
                                                                   glob=False)

        hash_collection, data_collection, database_collection = self.create_mocks()
        instance = Usage(hash_collection, data_collection, database_collection)

        database_paths = instance.get_database_paths()
        self.assertTrue(database_paths == ['test_input.txt'])

    @patch('Usage.UserArguments.argparse.ArgumentParser.parse_args')
    def test_get_database_paths_if_glob_true(self, command_line_arguments_mock):
        command_line_arguments_mock.return_value = SimpleNamespace(input='test_glob_dir',
                                                                   additional='test_additional.txt',
                                                                   glob=True)
        self.create_mocks()
        hash_collection, data_collection, database_collection = self.create_mock_collections()
        instance = Usage(hash_collection, data_collection, database_collection)

        database_paths = instance.get_database_paths()
        self.assertEqual([os.path.join('test_glob_dir', 'test_file.txt'),
                          os.path.join('test_glob_dir', 'test_file2.txt', )], database_paths)

    @patch('Usage.UserArguments.argparse.ArgumentParser.parse_args')
    @patch('Format.FileFormatDeterminer.FileFormatDeterminer.determine_file_format')
    def test_handle_database_if_valid_format_content(self, file_format_mock, command_line_arguments_mock):
        file_format_mock.return_value = FileFormat(['field1', 'field2', 'field3'], [], ',')
        command_line_arguments_mock.return_value = SimpleNamespace(input='test_input.txt',
                                                                   additional='test_additional.txt',
                                                                   glob=False,
                                                                   json=False,
                                                                   manual=True,
                                                                   skip_invalid_lines=False)
        hash_collection, data_collection, database_collection = self.create_mocks()
        instance = Usage(hash_collection, data_collection, database_collection)
        instance.handle_database('test_input.txt')
        expected_file_identifier = '26760818823f83ae3ced756d6ad666db7c6a1a6b62db9713c5adf3e3f376a6ec45d4f9370626e87aaeac1f051e5ed417c030eda59a5aba18dcbbf1854609ed9f'

        documents = hash_collection.count_documents({'hash': expected_file_identifier})
        self.assertNotEqual(documents, 0)

    @patch('Usage.UserArguments.argparse.ArgumentParser.parse_args')
    @patch('Format.FileFormatDeterminer.FileFormatDeterminer.determine_file_format')
    def test_handle_database_if_invalid_format_content(self, file_format_mock, command_line_arguments_mock):
        file_format_mock.return_value = FileFormat(['test1', 'test2'], [], ',')
        command_line_arguments_mock.return_value = SimpleNamespace(input='invalid_test_input.txt',
                                                                   additional='test_additional.txt',
                                                                   json=False,
                                                                   glob=False,
                                                                   manual=True,
                                                                   skip_invalid_lines=False)
        hash_collection, data_collection, database_collection = self.create_mocks()
        with self.assertRaises(SystemExit):
            instance = Usage(hash_collection, data_collection, database_collection)
            instance.handle_database('invalid_test_input.txt')

    def create_mocks(self):
        self.create_mock_files()
        return self.create_mock_collections()

    def create_mock_files(self):
        input_file_mock = "test_input.txt"
        input_file_contents = "1,2,3"
        self.create_fake_file(input_file_mock, input_file_contents)

        invalid_input_file_mock = "invalid_test_input.txt"
        invalid_input_file_contents = "1,2,3\n4,5,6\n7,8,9"
        self.create_fake_file(invalid_input_file_mock, invalid_input_file_contents)

        additional_information_file = "test_additional.txt"
        additional_information_contents = "database,entries,dumped\nexampledata,22222,2022-02-02"
        self.create_fake_file(additional_information_file, additional_information_contents)
        self.fs.create_dir('test_glob_dir')
        self.fs.create_file('test_glob_dir/test_file.txt')
        self.fs.create_file('test_glob_dir/test_file2.txt')

    def create_fake_file(self, file_path, file_contents):
        self.fs.create_file(file_path, contents=file_contents)

    @staticmethod
    def create_mock_collections():
        client = mongomock.MongoClient()
        database = client["test"]
        hash_collection = database["hash"]
        data_collection = database["data"]
        database_collection = database["database"]
        return hash_collection, data_collection, database_collection


if __name__ == '__main__':
    unittest.main()
