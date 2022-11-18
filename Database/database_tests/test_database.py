import os
import unittest

import pandas as pd

from Database.DatabaseCombiner import DatabaseCombiner


def get_relative_path_to_file(relative_path_to_file: str) -> str:
    dir_name = os.path.dirname(__file__)
    relative_path = os.path.join(dir_name, relative_path_to_file)
    return relative_path


class TestDatabase(unittest.TestCase):
    def setUp(self) -> None:
        self.testing_file_path = os.path.join('Database', 'database_tests', 'files', 'testing_file.txt')

    def test_get_breach_date_from_additional_database_information(self):
        additional_information_about_databases = pd.DataFrame(
            {'database': ["000webhost.com", "007.no"], 'entries': [15271696, 3834673],
             'dumped': ["2011-05-21", "2022-02-13"]})

        breach_date_related_to_database_name = additional_information_about_databases.loc[
            additional_information_about_databases['database'] == '000webhost.com', 'dumped'].item()
        self.assertEqual(breach_date_related_to_database_name, "2011-05-21")

    def test_raise_exception_when_database_does_not_exist(self):
        additional_information_about_databases = pd.DataFrame(
            {'database': [], 'entries': [],
             'dumped': []})

        # When a database is not found, it will throw a Value Error.
        with self.assertRaises(ValueError):
            additional_information_about_databases.loc[
                additional_information_about_databases['database'] == 'this_database_does_not_exist', 'dumped'].item()

    def test_set_additional_information_to_database(self):
        additional_information_about_databases = pd.DataFrame({'database': ["testing_file"], 'entries': [15271696],
                                                               'dumped': ["2011-05-21"]})

        our_loaded_database = DatabaseCombiner(additional_information_about_databases)

        database_contents = pd.DataFrame({'test': ["asd1"], 'test2': ["asd2"], 'test3': ["asd3"]})
        combined_database = our_loaded_database.combine(database_contents, self.testing_file_path)
        self.assertEqual("testing_file", combined_database["database_name"].item())
        self.assertEqual("2011-05-21", combined_database["breach_date"].item())


if __name__ == '__main__':
    unittest.main()
