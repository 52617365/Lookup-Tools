import unittest

import mongomock
import pandas as pd

from DatabaseWriter.AdditionalWriter import AdditionalWriter


class TestAdditionalWriter(unittest.TestCase):
    def setUp(self):
        client = mongomock.MongoClient().test.test_collection
        self.databases_collection = client.db.collection
        self.additional_information_about_databases = pd.DataFrame(
            {'database': ["test", "007.no"], 'entries': [15271696, 3834673],
             'dumped': ["2011-05-21", "2022-02-13"]})

    def test_write_additional_information_without_breach_date(self):
        writer = AdditionalWriter(self.databases_collection)
        writer.insert_database_additional_information("test222", 1, self.additional_information_about_databases)
        self.assertNotEqual(self.databases_collection.find_one({'database_name': {"$in": ["test222"]}}), None)
        self.assertEqual(self.databases_collection.find_one({'breach_date': {"$in": ["2020-01-01"]}}), None)

    def test_write_additional_information_with_breach_date(self):
        writer = AdditionalWriter(self.databases_collection)
        writer.insert_database_additional_information("test", 1, self.additional_information_about_databases)

        self.assertNotEqual(self.databases_collection.find_one({'database_name': {"$in": ["test"]}}), None)
        self.assertNotEqual(self.databases_collection.find_one({'breach_date': {"$in": ["2011-05-21"]}}), None)


if __name__ == '__main__':
    unittest.main()
