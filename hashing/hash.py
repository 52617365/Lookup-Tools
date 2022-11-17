import hashlib

from pandas import DataFrame


def get_sha256_hash_from(file_data: DataFrame) -> str:
    file_data = file_data.to_string()
    return hashlib.sha256(file_data.encode('utf-8')).hexdigest()
