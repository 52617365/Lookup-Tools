import os
import unittest

import pandas as pd

from hasher.hash import Hasher


class TestHashing(unittest.TestCase):
    def test_write_file_identifier_to_hashes(self):
        hashes_file_path = "test_hashes.txt"
        sha256_hash_to_expect = 'f90d860c5753d69b89d375e53ff8a9644f28c9ffe83cf1daa8de641d8d37ab07'

        csv_to_hash = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})

        hasher = Hasher(csv_to_hash, hashes_file_path)
        hasher.write_unique_identifier_of_file_to_logs()

        with open(hashes_file_path, "r") as hashes:
            sha256_hash = hashes.readline().rstrip()

        os.remove("test_hashes.txt")
        self.assertEqual(sha256_hash_to_expect, sha256_hash)

    def test_default_hash_file_name_gets_set(self):
        csv_to_hash = pd.DataFrame()
        hasher = Hasher(csv_to_hash)

        expected_default_hash_file_name = "file_hashes.txt"
        self.assertEqual(hasher.get_hash_file_path(), expected_default_hash_file_name)


if __name__ == '__main__':
    unittest.main()
