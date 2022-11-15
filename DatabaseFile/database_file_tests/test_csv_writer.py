import json
import os
import unittest

import pandas as pd

from DatabaseFile.database_writer import DatabaseWriter


def get_relative_path_to_file(relative_path_to_file: str) -> str:
    dir_name = os.path.dirname(__file__)
    relative_path = os.path.join(dir_name, relative_path_to_file)
    return relative_path


class TestCsvWriter(unittest.TestCase):
    hashes_file = "file_hashes.txt"

    def test_write_as_json(self):
        testing_file_path = get_relative_path_to_file('files/test.json')

        csv_data_to_write_as_json = pd.DataFrame({'dir': ["asd1"], 'test2': ["asd2"], 'test3': ["asd3"]})

        writer = DatabaseWriter(testing_file_path, csv_data_to_write_as_json, "")
        writer.write_as_json()

        file_handle_to_json_file = open(testing_file_path, "r")
        json_string_that_was_written = file_handle_to_json_file.read()

        file_handle_to_json_file.close()

        json.loads(json_string_that_was_written)

    def test_write_unique_identifier_of_valid_file(self):
        csv_to_hash = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})

        writer = DatabaseWriter("", csv_to_hash, self.hashes_file)
        writer.write_valid_file_hash_to_logs()

        with open(self.hashes_file, "r") as hashes:
            sha256_hash = hashes.readline().rstrip()

        sha256_hash_to_expect = 'f90d860c5753d69b89d375e53ff8a9644f28c9ffe83cf1daa8de641d8d37ab07'
        self.assertEqual(sha256_hash_to_expect, sha256_hash)

    def test_write_unique_identifier_of_invalid_file(self):
        csv_to_hash = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})

        writer = DatabaseWriter("", csv_to_hash, self.hashes_file)
        writer.write_invalid_file_hash_to_logs()

        with open(self.hashes_file, "r") as hashes:
            sha256_hash = hashes.readline().rstrip()

        sha256_hash_to_expect = 'f90d860c5753d69b89d375e53ff8a9644f28c9ffe83cf1daa8de641d8d37ab07'
        self.assertEqual(sha256_hash_to_expect, sha256_hash)

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.hashes_file)
        os.remove("invalid_" + cls.hashes_file)


if __name__ == '__main__':
    unittest.main()
