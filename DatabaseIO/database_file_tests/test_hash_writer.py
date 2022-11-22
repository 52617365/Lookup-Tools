import unittest

from pyfakefs.fake_filesystem_unittest import TestCase

from DatabaseIO.HashWriter import HashWriter


class TestHashWriter(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    def test_get_hash_from_file_contents(self):
        test_fake_file = self.create_fake_file("testing_file.txt", "field1,field2,field3\n1,2,3\n4,5,6")
        hash_from_file = HashWriter.get_hash_from_file_contents(test_fake_file)
        blake2b_hash_to_expect = '33a96dbac7cb421881236eebfddceea8fe6a3be6a73d1bbb0a17aee9a834440fd9f4b0bb0ca7a1792b711cb5dcf1ebdb621ec07a7b7fd97507e115efa7594cbf'
        self.assertEqual(blake2b_hash_to_expect, hash_from_file)

    def create_fake_file(self, testing_file_path: str, contents: str):
        self.fs.create_file(testing_file_path, contents=contents)
        return testing_file_path


if __name__ == '__main__':
    unittest.main()
