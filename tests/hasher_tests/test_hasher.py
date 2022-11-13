import os
import unittest

import pandas as pd

from hasher.hash import Hasher


class TestHashing(unittest.TestCase):
    def test_write_file_identifier_to_hashes(self):
        dir_name = os.path.dirname(__file__)
        testing_hashes_file_path = os.path.join(dir_name, 'files/test_hashes.txt')

        csv_to_hash = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})

        hasher = Hasher(csv_to_hash, testing_hashes_file_path)
        hasher.write_unique_identifier_of_file_to_logs()

        with open(testing_hashes_file_path, "r") as hashes:
            sha256_hash = hashes.readline().rstrip()

        os.remove(testing_hashes_file_path)

        sha256_hash_to_expect = 'f90d860c5753d69b89d375e53ff8a9644f28c9ffe83cf1daa8de641d8d37ab07'
        self.assertEqual(sha256_hash_to_expect, sha256_hash)

    def test_system_exit_if_no_hash_file_path_provided(self):
        with self.assertRaises(SystemExit):
            csv_to_hash = pd.DataFrame()
            hasher = Hasher(csv_to_hash)


if __name__ == '__main__':
    unittest.main()
