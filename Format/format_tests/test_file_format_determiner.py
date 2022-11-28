import unittest
from unittest.mock import patch

from pyfakefs.fake_filesystem_unittest import TestCase

from Format.FileFormatDeterminer import FileFormatDeterminer
from Format.format_tests.HiddenPrints import HiddenPrints


class TestFileFormatDeterminer(TestCase):
    def setUp(self) -> None:
        self.setUpPyfakefs()

    def test_ctor(self):
        file_format_determiner = FileFormatDeterminer("path", 5)
        self.assertEqual(file_format_determiner.database_path, "path")
        self.assertEqual(file_format_determiner.n, 5)

    def test_read_the_first_n_lines_from_file(self):
        self.fs.create_file("path", contents="line1\nline2\nline3\nline4\nline5\nline6\nline7\nline8\nline9\nline10")
        file_format_determiner = FileFormatDeterminer("path", n=5)
        self.assertEqual(["line1", "line2", "line3", "line4", "line5"],
                         file_format_determiner.read_the_first_n_lines_from_file_whilst_deleting_new_lines(),
                         )

    def test_determine_raises_exception_if_n_bigger_than_file_contents(self):
        self.fs.create_file("path", contents="line1\nline2")
        file_format_determiner = FileFormatDeterminer("path", n=5)
        with self.assertRaises(StopIteration):
            with HiddenPrints():
                file_format_determiner.determine_file_format()

    @patch('Format.FileFormatDeterminer.get_file_delimiter_from_user')
    @patch('Format.FileFormatDeterminer.get_file_fields_from_user')
    def test_determine_file_format_with_ignored_fields(self, file_fields_mock, file_delimiter_mock):
        file_fields_mock.return_value = ["field1", "field2", "_field3"]
        file_delimiter_mock.return_value = ","
        self.fs.create_file("path", contents="line1,line2,line3\nline4,line5,line6")
        file_format_determiner = FileFormatDeterminer("path", n=2)
        with HiddenPrints():
            file_format = file_format_determiner.determine_file_format()
        self.assertEqual(file_format.fields, ["field1", "field2", "_field3"])
        self.assertEqual(file_format.ignored_fields, ["_field3"])
        self.assertEqual(file_format.file_delimiter, ",")


if __name__ == '__main__':
    unittest.main()
