import unittest

import pandas as pd
from pyfakefs.fake_filesystem_unittest import TestCase

from DatabaseIO.JsonWriter import JsonWriter


class TestDatabaseWriter(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    def test_write_as_json(self):
        fake_file_name = "parsed/test.json"
        self.fs.create_file(fake_file_name)

        csv_data_to_write_as_json = pd.DataFrame({'dir': ["asd1"], 'test2': ["asd2"], 'test3': ["asd3"]})
        writer = JsonWriter(fake_file_name, csv_data_to_write_as_json)
        writer.write_as_json()

        expected_json_data = "[{\"dir\":\"asd1\",\"test2\":\"asd2\",\"test3\":\"asd3\"}]"

        with open(fake_file_name, 'r') as f:
            json_data = f.read()
            assert json_data == expected_json_data


if __name__ == '__main__':
    unittest.main()
