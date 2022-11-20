import json
import os
import unittest

import pandas as pd

from DatabaseIO.HashWriter import HashWriter


def get_relative_path_to_file(relative_path_to_file: str) -> str:
    dir_name = os.path.dirname(__file__)
    relative_path = os.path.join(dir_name, relative_path_to_file)
    return relative_path


class TestCsvWriter(unittest.TestCase):
    hashes_file = "file_hashes.txt"

    def test_pandas_dataframe_json_conversion(self):
        csv_data_to_write_as_json = pd.DataFrame({'dir': ["asd1"], 'test2': ["asd2"], 'test3': ["asd3"]})
        converted_json_data = csv_data_to_write_as_json.to_json(orient='records')
        json.loads(converted_json_data)

    def test_unique_identifier_gets_generated_correctly(self):
        csv_to_hash = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})

        generated_identifier = HashWriter.get_blake2b_hash_from(csv_to_hash)
        sha256_hash_to_expect = 'f90d860c5753d69b89d375e53ff8a9644f28c9ffe83cf1daa8de641d8d37ab07'
        self.assertEqual(sha256_hash_to_expect, generated_identifier)


if __name__ == '__main__':
    unittest.main()
