import unittest

from pyfakefs.fake_filesystem_unittest import TestCase

from Reader.Hash import Hash


class TestHash(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    def test_file_hashing_works(self):
        testing_file_path = self.create_fake_file("testing_file.csv", "asd1,asd2,asd3")
        expected_file_identifier = "bdc56b1c2845a0ff642efb5fc6c6acc35f5cdcc27036deb2493573356a57ce70ecaa72cb71a0b96134afb860519aea1f9ce4b4804478ae3b49f4ce0e4cbc270d"

        hash_result = Hash.get_hash_from_file_contents(testing_file_path)
        self.assertEqual(expected_file_identifier, hash_result)

    def create_fake_file(self, testing_file_path: str, contents: str):
        self.fs.create_file(testing_file_path, contents=contents)
        return testing_file_path


if __name__ == '__main__':
    unittest.main()
