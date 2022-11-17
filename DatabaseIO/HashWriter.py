import hashlib

from pandas import DataFrame


class HashWriter:
    def __init__(self, valid_hashes_file, invalid_hashes_file):
        self.valid_hashes_file = valid_hashes_file
        self.invalid_hashes_file = invalid_hashes_file

    @staticmethod
    def get_sha256_hash_from(data_to_write: DataFrame) -> str:
        file_data = data_to_write.to_string()
        return hashlib.sha256(file_data.encode('utf-8')).hexdigest()

    def write_valid_file_hash_to_logs(self, file_identifier: str):
        self.valid_hashes_file.write(file_identifier + "\n")

    def write_invalid_file_hash_to_logs(self, file_identifier: str):
        self.invalid_hashes_file.write(file_identifier + "\n")

    def file_is_unique(self, file_identifier: str) -> bool:
        return not self.__hash_is_already_in_hashes_file(file_identifier)

    def __hash_is_already_in_hashes_file(self, file_identifier: str):
        valid_hashes = self.valid_hashes_file.readlines()
        invalid_hashes = self.invalid_hashes_file.readlines()
        hashes = valid_hashes + invalid_hashes
        for line in hashes:
            if line.strip() == file_identifier:
                return True
        return False
