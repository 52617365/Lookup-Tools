import os
import unittest

import pandas as pd

from hasher.hash import Hasher


def get_relative_path_to_file(relative_path_to_file: str) -> str:
    dir_name = os.path.dirname(__file__)
    relative_path = os.path.join(dir_name, relative_path_to_file)

    return relative_path


# TODO: make a test for file_is_unique function.
class TestHasher(unittest.TestCase):
    def setUp(self):
        self.testing_hashes_file_path = get_relative_path_to_file('files/test_hashes.txt')
        self.testing_invalid_hashes_file_path = get_relative_path_to_file('files/invalid_test_hashes.txt')

    def test_write_unique_identifier_of_valid_file(self):
        csv_to_hash = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})

        hasher = Hasher(csv_to_hash, self.testing_hashes_file_path)
        hasher.write_valid_file_hash_to_logs()

        with open(self.testing_hashes_file_path, "r") as hashes:
            sha256_hash = hashes.readline().rstrip()

        os.remove(self.testing_hashes_file_path)

        sha256_hash_to_expect = 'f90d860c5753d69b89d375e53ff8a9644f28c9ffe83cf1daa8de641d8d37ab07'
        self.assertEqual(sha256_hash_to_expect, sha256_hash)

    def test_write_unique_identifier_of_invalid_file(self):
        csv_to_hash = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})

        hasher = Hasher(csv_to_hash, self.testing_hashes_file_path)
        hasher.write_invalid_file_hash_to_logs()

        with open(self.testing_invalid_hashes_file_path, "r") as hashes:
            sha256_hash = hashes.readline().rstrip()

        os.remove(self.testing_invalid_hashes_file_path)

        sha256_hash_to_expect = 'f90d860c5753d69b89d375e53ff8a9644f28c9ffe83cf1daa8de641d8d37ab07'
        self.assertEqual(sha256_hash_to_expect, sha256_hash)

    def test_system_exit_if_no_hash_file_path_provided(self):
        with self.assertRaises(SystemExit):
            csv_to_hash = pd.DataFrame()
            Hasher(csv_to_hash)


if __name__ == '__main__':
    unittest.main()
