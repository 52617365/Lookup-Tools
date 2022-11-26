import unittest

import mongomock
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

        writer = JsonWriter(csv_data, data_collection, None)
        writer.insert_database_contents_as_json()
        self.assertTrue(data_collection.find_one({'dir': "asd1"}, {'_id': 1}))

    def test_write_additional_information_with_breach_date(self):
        client = mongomock.MongoClient().test.test_collection
        databases_collection = client.db.collection

        csv_data = pd.DataFrame({"database_name": ["test"], "breach_date": ["2020-01-01"]})

        writer = JsonWriter(csv_data, None, databases_collection)
        writer.insert_database_additional_information()

        self.assertNotEqual(databases_collection.find_one({'database_name': {"$in": ["test"]}}), None)
        self.assertNotEqual(databases_collection.find_one({'breach_date': {"$in": ["2020-01-01"]}}), None)

    def test_write_additional_information_without_breach_date(self):
        client = mongomock.MongoClient().test.test_collection
        databases_collection = client.db.collection

        csv_data = pd.DataFrame({"database_name": ["test"]})

        writer = JsonWriter(csv_data, None, databases_collection)
        writer.insert_database_additional_information()
        self.assertNotEqual(databases_collection.find_one({'database_name': {"$in": ["test"]}}), None)
        self.assertEqual(databases_collection.find_one({'breach_date': {"$in": ["2020-01-01"]}}), None)


if __name__ == '__main__':
    unittest.main()
