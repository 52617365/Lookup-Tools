import unittest

import mongomock
import numpy as np
import pandas as pd
from pyfakefs.fake_filesystem_unittest import TestCase

from DatabaseWriter.JsonWriter import JsonWriter


class TestJsonWriter(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    def test_write_as_json(self):
        client = mongomock.MongoClient().test.test_collection
        data_collection = client.db.collection

        csv_data = pd.DataFrame({'dir': ["asd1"], 'test2': ["asd2"], 'test3': ["asd3"]})

        writer = JsonWriter(csv_data, data_collection)
        writer.insert_database_contents_as_json()
        self.assertTrue(data_collection.find_one({'dir': "asd1"}, {'_id': 1}))

    def test_nan_values_get_deleted(self):
        data = [{'test1': np.NaN, 'test2': 2, 'test3': 3}, {'test1': 1, 'test2': 2, 'test3': np.NaN}]
        JsonWriter.delete_nan_values(data)

        expected_data = [{'test2': 2, 'test3': 3}, {'test1': 1, 'test2': 2}]
        self.assertEqual(data, expected_data)


if __name__ == '__main__':
    unittest.main()
