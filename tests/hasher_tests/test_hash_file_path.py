import os
import unittest
from unittest import mock

from hasher.hash_file_path import HashFilePath


class TestHashFilePath(unittest.TestCase):
    def test_raise_exception_if_env_var_set_but_empty(self):
        with self.assertRaises(SystemExit):
            with mock.patch.dict(os.environ, {"HASH_FILE_PATH": ""}):
                HashFilePath().get()

    def test_env_variable_gets_picked_if_no_user_specified_path_provided(self):
        dir_name = os.path.dirname(__file__)
        expected_file_path = os.path.join(dir_name, 'files/example_hash_file_path.txt')
        with mock.patch.dict(os.environ, {"HASH_FILE_PATH": expected_file_path}):
            file_path = HashFilePath().get()
            self.assertEqual(file_path, expected_file_path)

    def test_user_specified_gets_picked_if_its_provided(self):
        dir_name = os.path.dirname(__file__)
        expected_file_path = os.path.join(dir_name, 'files/example_hash_file_path.txt')
        file_path = HashFilePath(expected_file_path).get()
        self.assertEqual(file_path, expected_file_path)

    def test_system_exit_happens_if_nothing_is_provided(self):
        with self.assertRaises(SystemExit):
            HashFilePath().get()


if __name__ == '__main__':
    unittest.main()
