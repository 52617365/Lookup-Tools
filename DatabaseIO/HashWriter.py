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
        config = dotenv_values(F"{current_path}\\.env")
        HashWriterConnection.__terminate_if_env_values_invalid(config)
        return config

    @staticmethod
    def __terminate_if_env_values_invalid(config: dict):
        required_keys = ['DATABASE_NAME', 'COLLECTION_NAME', 'CONNECTION_STRING']

        for key in required_keys:
            if config[key] is None:
                quit("Missing key in .env file: " + key)


class HashWriter:
    def __init__(self):
        self.mongo_hash_collection = HashWriterConnection().collection

    def write_valid_hash(self, hash):
        if self.hash_is_unique(hash):
            self.mongo_hash_collection.insert_one({"hash": hash, "valid": True})

    def write_invalid_hash(self, hash):
        if self.hash_is_unique(hash):
            self.mongo_hash_collection.insert_one({"hash": hash, "valid": False})

    def hash_is_unique(self, hash: str):
        return self.mongo_hash_collection.find_one({"hash": hash}) is None

    @staticmethod
    def get_sha256_hash_from(data_to_write: DataFrame) -> str:
        file_data = data_to_write.to_string()
        return hashlib.sha256(file_data.encode('utf-8')).hexdigest()
