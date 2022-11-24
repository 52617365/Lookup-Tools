import os
import unittest
from types import SimpleNamespace
from unittest.mock import patch

import mongomock
import pandas as pd
from pyfakefs.fake_filesystem_unittest import TestCase

from Usage.usage import Usage


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

        self.assertTrue(instance.additional_information.equals(pd.DataFrame({"field": ["value"]})))
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
        self.assertEqual(database_paths,
                         [os.path.join('test_glob_dir', 'test_file.txt'),
                          os.path.join('test_glob_dir', 'test_file2.txt', )])

    def create_mocks(self):
        self.create_mock_files()
        return self.create_mock_collections()

    def create_mock_files(self):
        input_file_mock = "test_input.txt"
        input_file_contents = "test1,test2,test3\n1,2,3"
        self.create_fake_file(input_file_mock, input_file_contents)
        additional_information_file = "test_additional.txt"
        additional_information_contents = "field\nvalue"
        self.create_fake_file(additional_information_file, additional_information_contents)
        self.fs.create_dir('test_glob_dir')
        self.fs.create_file('test_glob_dir/test_file.txt')
        self.fs.create_file('test_glob_dir/test_file2.txt')

    @staticmethod
    def create_mock_collections():
        client = mongomock.MongoClient()
        database = client["test"]
        hash_collection = database["hash"]
        data_collection = database["data"]
        database_collection = database["database"]
        return hash_collection, data_collection, database_collection

    def create_fake_file(self, file_path, file_contents):
        self.fs.create_file(file_path, contents=file_contents)


if __name__ == '__main__':
    unittest.main()
