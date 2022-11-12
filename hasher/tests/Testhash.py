import os
import unittest

import pandas as pd

from hasher.hash import Hasher


class TestHashing(unittest.TestCase):
    def test_write_file_identifier_to_hashes(self):
        hashes_file_path = "test_hashes.txt"
        sha256_hash_to_expect = 'f90d860c5753d69b89d375e53ff8a9644f28c9ffe83cf1daa8de641d8d37ab07'

        csv_to_hash = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})

        hasher = Hasher(csv_to_hash.to_csv(), hash_file_path="test_hashes.txt")
        hasher.write_file_identifier_to_hashes()

        with open(hashes_file_path, "r") as hashes:
            sha256_hash = hashes.readline().rstrip()

        os.remove("test_hashes.txt")
        self.assertEqual(sha256_hash_to_expect, sha256_hash)


if __name__ == '__main__':
    unittest.main()
