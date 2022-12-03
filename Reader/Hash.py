import hashlib


class Hash:
    def __init__(self, path_to_file: str):
        self.path_to_file = path_to_file

    def get_hash_from_file_contents(self) -> str:
        try:
            with open(self.path_to_file, "rb") as file:
                file_contents = file.read()
                return self.__get_blake2b_hash_from(file_contents)
        except OSError:
            quit("Could not open file: " + self.path_to_file)

    @staticmethod
    def __get_blake2b_hash_from(file_data: bytes) -> str:
        file_hash = hashlib.blake2b(file_data).hexdigest()
        return file_hash
