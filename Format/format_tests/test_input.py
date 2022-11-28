import unittest
from unittest.mock import patch

from Format.Input import get_file_fields_from_user, get_file_delimiter_from_user, IDKException


class TestInput(unittest.TestCase):

    @patch("builtins.input")
    def test_get_valid_file_format_from_user(self, user_input):
        user_input.return_value = "field1,field2,field3"
        file_format = get_file_fields_from_user()
        self.assertEqual(file_format, ["field1", "field2", "field3"])

    @patch("builtins.input")
    def test_get_invalid_file_format_from_user(self, user_input):
        user_input.return_value = ""
        with self.assertRaises(SystemExit):
            get_file_fields_from_user()

    @patch("builtins.input")
    def test_get_file_format_from_user_with_one_field(self, user_input):
        user_input.return_value = "field"
        file_format = get_file_fields_from_user()
        self.assertEqual(file_format, ["field"])

    @patch("builtins.input")
    def test_exception_raised_if_file_format_is_idk(self, user_input):
        user_input.return_value = "idk"
        with self.assertRaises(IDKException):
            get_file_fields_from_user()

    @patch("builtins.input")
    def test_get_invalid_file_delimiter_from_user(self, user_input):
        with self.assertRaises(SystemExit):
            user_input.return_value = ",,"
            get_file_delimiter_from_user()

    @patch("builtins.input")
    def test_get_valid_file_delimiter_from_user(self, user_input):
        valid_delimiters = ["|", ",", ";", ":", " ", "\t"]
        for delimiter in valid_delimiters:
            user_input.return_value = delimiter
            self.assertEqual(get_file_delimiter_from_user(), delimiter)

    @patch("builtins.input")
    def test_exception_raised_if_file_delimiter_is_idk(self, user_input):
        user_input.return_value = "idk"
        with self.assertRaises(IDKException):
            get_file_delimiter_from_user()


if __name__ == '__main__':
    unittest.main()
