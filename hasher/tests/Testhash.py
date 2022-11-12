import os
import unittest

import pandas as pd

from hasher.hash import Hasher


class TestHashing(unittest.TestCase):
    def test_write_file_identifier_to_hashes(self):
        hashes_file_path = "test_hashes.txt"
        sha256_hash_to_expect = '0135f96620e9f8580565621014f1d4acad1288033562c92dc9eef504fbdffe80'

        csv_to_hash = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})

        hasher = Hasher(csv_to_hash.to_csv(), hash_file_path="test_hashes.txt")
        hasher.write_file_identifier_to_hashes()

        with open(hashes_file_path, "r") as hashes:
            sha256_hash = hashes.readline().rstrip()

        os.remove("test_hashes.txt")
        self.assertEqual(sha256_hash, sha256_hash_to_expect)


if __name__ == '__main__':
    unittest.main()
