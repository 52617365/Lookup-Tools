import unittest

import mongomock
import pandas as pd
from pyfakefs.fake_filesystem_unittest import TestCase

from DatabaseWriter.JsonWriter import JsonWriter


class TestDatabaseWriter(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    def test_write_as_json(self):
        client = mongomock.MongoClient().test.test_collection
        collection = client.db.collection

        csv_data = pd.DataFrame({'dir': ["asd1"], 'test2': ["asd2"], 'test3': ["asd3"]})

        writer = JsonWriter(csv_data, collection)
        writer.write_as_json()
        self.assertTrue(collection.find_one({'dir': "asd1"}, {'_id': 1}))


if __name__ == '__main__':
    unittest.main()
