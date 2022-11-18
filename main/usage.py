import pandas as pd

from Database.DatabaseCombiner import DatabaseCombiner
from DatabaseIO.HashWriter import HashWriter
from DatabaseIO.JsonWriter import JsonWriter
from FileGlob.FileGlob import FileGlob
from main.UserArguments import CommandLineArguments


def get_databases(args):
    if args.glob:
        databases = FileGlob(args.input).get_files_from_directories()
    else:
        databases = [args.input]

    return databases


if __name__ == '__main__':
    args = CommandLineArguments().get()
    databases = get_databases(args)
    additional_information = pd.read_csv(args.additional_information)
    hash_writer = HashWriter("file_hashes.txt")

    for database in databases:
        sha256_for_database = HashWriter.get_sha256_hash_from(database)
        if not hash_writer.file_is_unique(sha256_for_database):
            continue

        try:
            combined_delimited_database = DatabaseCombiner(additional_information).combine(database)
            database_writer = JsonWriter(DatabaseCombiner.get_file_name(database), combined_delimited_database)
            hash_writer.write_valid_file_hash_to_logs(sha256_for_database)
        except Exception as e:
            hash_writer.write_invalid_file_hash_to_logs(sha256_for_database)
