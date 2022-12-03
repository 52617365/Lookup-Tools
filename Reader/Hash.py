import hashlib


class Hash:
    def __init__(self, path_to_file: str):
        self.path_to_file = path_to_file

    def get_hash_from_file_contents(self) -> str:
        try:
            with open(self.path_to_file, "rb") as file:
                blake2b_hash = self.get_hash_from_file_chunks(file)
                return blake2b_hash
        except OSError:
            quit("Could not open file: " + self.path_to_file)

    @staticmethod
    def get_hash_from_file_chunks(file) -> str:
        blake2b_hash = hashlib.blake2b()
        for chunk in iter(lambda: file.read(128 * blake2b_hash.block_size), b""):
            blake2b_hash.update(chunk)
        return blake2b_hash.hexdigest()

    # @staticmethod
    # def __get_blake2b_hash_from(file_data: bytes) -> str:
    #     file_hash = hashlib.blake2b(file_data).hexdigest()
    #     return file_hash
