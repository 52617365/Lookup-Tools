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

        input_file_mock = "test_input.txt"
        input_file_contents = "test1,test2,test3\n1,2,3"
        self.create_fake_file(input_file_mock, input_file_contents)

        additional_information_file = "test_additional.txt"
        additional_information_contents = "field\nvalue"
        self.create_fake_file(additional_information_file, additional_information_contents)

        hash_collection, data_collection, database_collection = self.create_mock_collections()
        instance = Usage(hash_collection, data_collection, database_collection)

        self.assertEqual(instance.additional_information.equals(pd.DataFrame({"field": ["value"]})), True)
        self.assertEqual(instance.hash_writer.mongo_hash_collection, hash_collection)

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
