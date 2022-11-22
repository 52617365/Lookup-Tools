import unittest
from unittest.mock import patch

import pandas as pd
from pyfakefs.fake_filesystem_unittest import TestCase

from DatabaseIO.HashWriter import HashWriter


class TestHashWriterConnection(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    def test_terminate_if_variables(self):
        with self.assertRaises(SystemExit):
            HashWriter()

    @patch('DatabaseIO.HashWriter.dotenv_values')
    def test_terminate_if_mongodb_does_not_exist(self, dotenv_values):
        dotenv_values.return_value = {"CONNECTION_STRING": "test_connection_string",
                                      "DATABASE_NAME": "test_database_name",
                                      "COLLECTION_NAME": "test_collection_name"}
        with self.assertRaises(SystemExit):
            HashWriter()


class TestHashWriter(unittest.TestCase):
    def test_unique_identifier_gets_generated_correctly(self):
        csv_to_hash = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})

        generated_identifier = HashWriter.get_blake2b_hash_from(csv_to_hash.to_string())
        blake2b_hash_to_expect = '85b57344812b6b8641055d21e5ffd1292ab849fba40d531e94dbf8910ff93f37422c969ec4830634f84a7efb8d7e3981f82f698009f841589ac05eaf97936e62'
        self.assertEqual(blake2b_hash_to_expect, generated_identifier)


if __name__ == '__main__':
    unittest.main()
