import os
import unittest
from unittest import mock

from hashing.hash_file_path import HashFilePath


def get_relative_file(relative_path_to_file: str) -> str:
    dir_name = os.path.dirname(__file__)
    relative_path = os.path.join(dir_name, relative_path_to_file)
    return relative_path


class TestHashFilePath(unittest.TestCase):
    def setUp(self):
        self.hash_hash_file_path_environment_variable = "HASH_FILE_PATH"
        self.invalid_hash_file_test_path = get_relative_file(
            "files/invalid_example_hash_file_path.txt")
        self.test_hash_file_path = get_relative_file(
            "files/example_hash_file_path.txt")

    def test_raise_exception_if_env_var_set_but_empty(self):
        with self.assertRaises(SystemExit):
            with mock.patch.dict(os.environ, {self.hash_hash_file_path_environment_variable: ""}):
                HashFilePath().get()

    def test_env_variable_gets_picked_if_no_user_specified_path_provided(self):
        with mock.patch.dict(os.environ,
                             {self.hash_hash_file_path_environment_variable: self.test_hash_file_path}):
            file_path = HashFilePath().get()
            self.assertEqual(file_path, self.test_hash_file_path)

    def test_user_specified_gets_picked_if_its_provided(self):
        file_path = HashFilePath(self.test_hash_file_path).get()
        self.assertEqual(file_path, self.test_hash_file_path)

    def test_system_exit_happens_if_nothing_is_provided(self):
        with self.assertRaises(SystemExit):
            HashFilePath().get()

    def test_invalid_hashes_file_gets_generated_in_the_same_directory_as_the_valid_hashes_file(self):
        dir_name = os.path.dirname(__file__)

        expected_file_path = os.path.join(dir_name, self.test_hash_file_path)

        HashFilePath(expected_file_path).get()

        invalid_hashes_path_exists = os.path.exists(self.invalid_hash_file_test_path)

        os.remove(self.invalid_hash_file_test_path)

        self.assertEqual(invalid_hashes_path_exists, True)


if __name__ == '__main__':
    unittest.main()
