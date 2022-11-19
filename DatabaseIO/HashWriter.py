import hashlib
import pathlib

import pymongo
from dotenv import dotenv_values
from pandas import DataFrame


class HashWriterConnection:
    def __init__(self):
        env = self.get_mongodb_env_variables()
        client = pymongo.MongoClient(env["CONNECTION_STRING"])
        database = client[env["DATABASE_NAME"]]
        self.collection = database[env["COLLECTION_NAME"]]

    @staticmethod
    def get_mongodb_env_variables():
        current_path = pathlib.Path(__file__).parent.resolve()
        config = dotenv_values(F"{current_path}\.env")
        HashWriterConnection.__terminate_if_env_values_invalid(config)
        return config

    @staticmethod
    def __terminate_if_env_values_invalid(config: dict):
        required_keys = ['DATABASE_NAME', 'COLLECTION_NAME', 'CONNECTION_STRING']

        for key in required_keys:
            if config[key] is None:
                quit("Missing key in .env file: " + key)

# TODO: change this to use a database.
class HashWriter:
    def __init__(self, path_to_valid_hashes: str):
        self.new_valid_hashes = set()
        self.new_invalid_hashes = set()
        self.valid_hashes_writer = self.open_write_handler_to_file(path_to_valid_hashes)
        self.invalid_hashes_writer = self.open_write_handler_to_invalid_file(path_to_valid_hashes)
        self.previous_hashes = self.get_previous_hashes(path_to_valid_hashes)

    @staticmethod
    def get_previous_hashes(path_to_valid_hashes: str):
        valid_hashes = HashWriter.read_contents_of_file(path_to_valid_hashes)
        invalid_hashes = HashWriter.read_contents_of_invalid_file(path_to_valid_hashes)
        return valid_hashes + invalid_hashes

    @staticmethod
    def read_contents_of_invalid_file(path_to_valid_hashes: str):
        invalid_hashes_file = get_file_name_for_invalid_hashes_file(path_to_valid_hashes)
        return HashWriter.read_contents_of_file(invalid_hashes_file)

    @staticmethod
    def read_contents_of_file(path_to_hashes: str):
        with open(path_to_hashes, "r") as file:
            return file.read().splitlines()

    @staticmethod
    def open_write_handler_to_invalid_file(path_to_valid_hashes: str):
        path_to_invalid_hashes = get_file_name_for_invalid_hashes_file(path_to_valid_hashes)
        handler_to_invalid_files = HashWriter.open_write_handler_to_file(path_to_invalid_hashes)
        return handler_to_invalid_files

    @staticmethod
    def open_write_handler_to_file(path_to_hashes: str):
        try:
            handler = open(path_to_hashes, "a", encoding='utf-8')
            return handler
        except IOError:
            quit(F"Hash file directory does not exist: {path_to_hashes}")

    @staticmethod
    def get_sha256_hash_from(data_to_write: DataFrame) -> str:
        file_data = data_to_write.to_string()
        return hashlib.sha256(file_data.encode('utf-8')).hexdigest()

    def write_hashes_to_file(self):
        self.write_valid_file_hashes_to_logs()
        self.write_invalid_file_hashes_to_logs()

    def write_valid_file_hashes_to_logs(self):
        HashWriter.write_set_to_file(self.valid_hashes_writer, self.new_valid_hashes)

    def write_invalid_file_hashes_to_logs(self):
        HashWriter.write_set_to_file(self.invalid_hashes_writer, self.new_invalid_hashes)

    @staticmethod
    def write_set_to_file(file_handler, contents_to_write: set):
        for content in contents_to_write:
            file_handler.write(content + "\n")
        file_handler.close()

    def file_is_unique(self, file_identifier: str) -> bool:
        if self.__hash_is_already_in_hashes_file(file_identifier):
            return False
        return True

    def __hash_is_already_in_hashes_file(self, file_identifier: str):
        if file_identifier in self.previous_hashes:
            return True
        return False
