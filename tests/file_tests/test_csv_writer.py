import json
import os
import unittest

import pandas as pd

from file.csvwriter import CsvWriter


class TestCsvWriter(unittest.TestCase):
    def test_write_as_json(self):
        dir_name = os.path.dirname(__file__)
        testing_file_path = os.path.join(dir_name, 'files/test.json')

        csv_data_to_write_as_json = pd.DataFrame({'test': ["asd1"], 'test2': ["asd2"], 'test3': ["asd3"]})

        writer = CsvWriter(testing_file_path, csv_data_to_write_as_json)
        writer.write_as_json()

        file_handle_to_json_file = open(testing_file_path, "r")
        json_string_that_was_written = file_handle_to_json_file.read()

        file_handle_to_json_file.close()

        json.loads(json_string_that_was_written)

    def test_write_as_csv(self):
        dir_name = os.path.dirname(__file__)
        testing_file_path = os.path.join(dir_name, 'files/test.csv')

        csv_file = pd.DataFrame({'test': ["asd1"], 'test2': ["asd2"], 'test3': ["asd3"]})

        writer = CsvWriter(testing_file_path, csv_file)
        writer.write_as_csv()

        written_csv_file = pd.read_csv(testing_file_path)

        expected_csv_data = pd.DataFrame({'test': ["asd1"], 'test2': ["asd2"], 'test3': ["asd3"]})

        self.assertEqual(written_csv_file.equals(expected_csv_data), True)


if __name__ == '__main__':
    unittest.main()
