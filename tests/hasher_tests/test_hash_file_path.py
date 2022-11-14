import os
import unittest
from unittest import mock

from hasher.hash_file_path import HashFilePath


class TestHashFilePath(unittest.TestCase):
    dir_name = os.path.dirname(__file__)
    expected_file_path = os.path.join(dir_name, 'example_hash_file_path.txt')

    def test_env_variable_gets_picked_if_no_user_specified_path_provided(self):
        with mock.patch.dict(os.environ, {"HASH_FILE_PATH": TestHashFilePath.expected_file_path}):
            file_path = HashFilePath().get()
            self.assertEqual(file_path, TestHashFilePath.expected_file_path)
            os.remove(TestHashFilePath.expected_file_path)

    def test_user_specified_gets_picked_if_its_provided(self):
        file_path = HashFilePath(TestHashFilePath.expected_file_path).get()
        self.assertEqual(file_path, TestHashFilePath.expected_file_path)
        os.remove(TestHashFilePath.expected_file_path)

    def test_system_exit_happens_if_nothing_is_provided(self):
        with self.assertRaises(SystemExit):
            HashFilePath().get()

    def test_invalid_hashes_file_gets_generated_in_the_same_directory_as_the_valid_hashes_file(self):
        dir_name = os.path.dirname(__file__)
        expected_invalid_hashes_directory = os.path.join(dir_name, 'files/invalid_example_hash_file_path.txt')
        expected_file_path = os.path.join(dir_name, 'files/example_hash_file_path.txt')

        HashFilePath(expected_file_path).get()

        invalid_hashes_path_exists = os.path.exists(expected_invalid_hashes_directory)

        os.remove(expected_invalid_hashes_directory)

        self.assertEqual(invalid_hashes_path_exists, True)


if __name__ == '__main__':
    unittest.main()
