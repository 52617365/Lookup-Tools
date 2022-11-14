import json
import os
import unittest

import pandas as pd

from file.csv_writer import CsvWriter


def get_relative_path_to_file(relative_path_to_file: str) -> str:
    dir_name = os.path.dirname(__file__)
    relative_path = os.path.join(dir_name, relative_path_to_file)
    return relative_path


class TestCsvWriter(unittest.TestCase):

    def test_write_as_json(self):
        testing_file_path = get_relative_path_to_file('files/test.json')

        csv_data_to_write_as_json = pd.DataFrame({'test': ["asd1"], 'test2': ["asd2"], 'test3': ["asd3"]})

        writer = CsvWriter(testing_file_path, csv_data_to_write_as_json)
        writer.write_as_json()

        file_handle_to_json_file = open(testing_file_path, "r")
        json_string_that_was_written = file_handle_to_json_file.read()

        file_handle_to_json_file.close()

        json.loads(json_string_that_was_written)

    def test_write_as_csv(self):
        testing_file_path = get_relative_path_to_file('files/test.csv')

        csv_file = pd.DataFrame({'test': ["asd1"], 'test2': ["asd2"], 'test3': ["asd3"]})

        writer = CsvWriter(testing_file_path, csv_file)
        writer.write_as_csv()

        written_csv_file = pd.read_csv(testing_file_path)

        expected_csv_data = pd.DataFrame({'test': ["asd1"], 'test2': ["asd2"], 'test3': ["asd3"]})

        self.assertEqual(written_csv_file.equals(expected_csv_data), True)


if __name__ == '__main__':
    unittest.main()
