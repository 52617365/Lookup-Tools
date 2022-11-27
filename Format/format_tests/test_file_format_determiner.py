import unittest

from pyfakefs.fake_filesystem_unittest import TestCase

from Format.DetermineFormat import FileFormatDeterminer


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
            file_format_determiner.determine()


if __name__ == '__main__':
    unittest.main()
