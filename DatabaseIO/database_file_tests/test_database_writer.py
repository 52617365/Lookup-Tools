import json
import unittest

import pandas as pd

from DatabaseIO.HashWriter import HashWriter


class TestDatabaseWriter(unittest.TestCase):
    def test_pandas_dataframe_json_conversion(self):
        csv_data_to_write_as_json = pd.DataFrame({'dir': ["asd1"], 'test2': ["asd2"], 'test3': ["asd3"]})
        converted_json_data = csv_data_to_write_as_json.to_json(orient='records')
        json.loads(converted_json_data)

    def test_unique_identifier_gets_generated_correctly(self):
        csv_to_hash = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})

        generated_identifier = HashWriter.get_blake2b_hash_from(csv_to_hash.to_string())
        blake2b_hash_to_expect = '85b57344812b6b8641055d21e5ffd1292ab849fba40d531e94dbf8910ff93f37422c969ec4830634f84a7efb8d7e3981f82f698009f841589ac05eaf97936e62'
        self.assertEqual(blake2b_hash_to_expect, generated_identifier)


if __name__ == '__main__':
    unittest.main()
