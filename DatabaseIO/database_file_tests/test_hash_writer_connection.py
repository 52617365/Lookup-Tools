from unittest.mock import patch

from pyfakefs.fake_filesystem_unittest import TestCase

from DatabaseIO.HashWriter import HashWriter


class TestHashWriterConnection(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    def test_terminate_if_variables(self):
        with self.assertRaises(SystemExit):
            HashWriter()

    @patch('DatabaseIO.HashWriter.dotenv_values')
    def test_terminate_if_mongodb_does_not_exist(self, dotenv_values):
        dotenv_values.return_value = {"CONNECTION_STRING": "test_connection_string",
                                      "DATABASE_NAME": "test_database_name",
                                      "COLLECTION_NAME": "test_collection_name"}
        with self.assertRaises(SystemExit):
            HashWriter()
