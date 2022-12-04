import hashlib


class Hash:
    @staticmethod
    def get_hash_from_file_contents(path_to_file: str) -> str:
        print(F"Generating hash from file: {path_to_file}.")
        try:
            with open(path_to_file, "rb") as file:
                blake2b_hash = Hash.get_hash_from_file_chunks(file)
                print(F"Generated hash for {path_to_file}.")
                return blake2b_hash
        except OSError:
            quit("Could not open file: " + path_to_file)

    @staticmethod
    def get_hash_from_file_chunks(file_handler) -> str:
        blake2b_hash = hashlib.blake2b()
        for chunk in iter(lambda: file_handler.read(100000 * blake2b_hash.block_size), b""):
            blake2b_hash.update(chunk)
        return blake2b_hash.hexdigest()
