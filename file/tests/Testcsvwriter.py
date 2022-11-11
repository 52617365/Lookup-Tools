import unittest

import pandas as pd

from file.filereader import FileReader


class MyTestCase(unittest.TestCase):
    def test_get_file_as_csv(self):
        file = FileReader("testing_file.txt")
        data = file.get_file_as_csv()
        df = pd.DataFrame({'test': ["asd1"], 'test2': ["asd2"], 'test3': ["asd3"]})
        self.assertEqual(data.equals(df), True)

    def test_get_file_as_csv_with_file_that_does_not_exist(self):
        with self.assertRaises(IOError):
            FileReader("file_that_does_not_exist.csv")


if __name__ == '__main__':
    unittest.main()
