import hashlib

from Database.DatabaseCombiner import get_file_name_from_path


class HashWriter:
    def __init__(self, mongo_hash_collection):
        self.mongo_hash_collection = mongo_hash_collection

    def write_valid_hash(self, hash: str, database_path: str):
        database_name = get_file_name_from_path(database_path)
        if self.hash_is_unique(hash):
            self.mongo_hash_collection.insert_one({"hash": hash, "database_name": database_name})

    def hash_is_unique(self, hash: str):
        return self.mongo_hash_collection.find_one({"hash": hash}) is None

    @staticmethod
    def get_hash_from_file_contents(path_to_file: str):
        try:
            with open(path_to_file, "r") as file:
                file_contents = file.read()
                return HashWriter.__get_blake2b_hash_from(file_contents)
        except OSError:
            quit("Could not open file: " + path_to_file)

    @staticmethod
    def __get_blake2b_hash_from(file_data: str) -> str:
        file_hash = hashlib.blake2b(file_data.encode('utf-8')).hexdigest()
        return file_hash
