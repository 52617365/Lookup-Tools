import pathlib

import pymongo
from dotenv import dotenv_values
from pymongo.errors import ServerSelectionTimeoutError


class HashWriterConnection:
    def __init__(self):
        env = self.get_mongodb_env_variables()
        self.collection = self.__get_mongo_collection(env)

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
            if config.get(key) is None:
                quit("Missing key in .env file: " + key)

    @staticmethod
    def __get_mongo_collection(config: dict):
        try:
            client = pymongo.MongoClient(config.get("CONNECTION_STRING"), serverSelectionTimeoutMS=10)
            client.server_info()
            database = client[config.get("DATABASE_NAME")]
            collection = database[config.get("COLLECTION_NAME")]
            return collection
        except ServerSelectionTimeoutError:
            quit("Unable to connect to MongoDB")
