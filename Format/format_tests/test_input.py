import unittest
from unittest.mock import patch

from Format.Input import get_file_fields_from_user, get_file_delimiter_from_user, IDKException, \
    terminate_if_user_did_not_specify_format, terminate_if_user_provided_invalid_file_fields, validate_user_input
from Format.format_tests.HiddenPrints import HiddenPrints


class TestInput(unittest.TestCase):

    @patch("builtins.input")
    def test_get_valid_file_format_from_user(self, user_input):
        user_input.return_value = "username,password,email"
        file_format = get_file_fields_from_user()
        self.assertEqual(file_format, ["username", "password", "email"])

    @patch("builtins.input")
    def test_get_invalid_file_format_from_user(self, user_input):
        user_input.return_value = ""
        with self.assertRaises(SystemExit):
            get_file_fields_from_user()

    @patch("builtins.input")
    def test_get_file_format_from_user_with_one_field(self, user_input):
        user_input.return_value = "username"
        file_format = get_file_fields_from_user()
        self.assertEqual(file_format, ["username"])

    @patch("builtins.input")
    def test_exception_raised_if_file_format_is_idk(self, user_input):
        user_input.return_value = "idk"
        with self.assertRaises(IDKException):
            get_file_fields_from_user()

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

    def test_terminate_if_user_did_not_specify_format(self):
        with self.assertRaises(SystemExit):
            terminate_if_user_did_not_specify_format("")

    def test_terminate_if_user_provided_invalid_file_fields(self):
        with self.assertRaises(SystemExit):
            with HiddenPrints():
                terminate_if_user_provided_invalid_file_fields("username,password,invalid_field")

    def test_dont_terminate_if_valid_input(self):
        validate_user_input("username,password,email")

    def test_dont_terminate_if_user_provided_ignored_fields_with_wrong_field(self):
        user_input = "username,password,email,_invalid_field"
        # assert doesnt raise exception
        terminate_if_user_provided_invalid_file_fields(user_input)


if __name__ == '__main__':
    unittest.main()
