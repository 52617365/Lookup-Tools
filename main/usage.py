import pandas as pd

from Database.DatabaseCombiner import DatabaseCombiner
from DatabaseIO.DatabaseReader import DatabaseReader
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


# TODO: We are currently not checking for if the file is invalid, fix this.

def get_additional_information():
    try:
        additional_information = pd.read_csv(args.additional)
        return additional_information
    except FileNotFoundError:
        quit("Additional information file not found")


if __name__ == '__main__':
    args = CommandLineArguments().get()
    additional_information = get_additional_information()
    databases = get_databases(args)
    hash_writer = HashWriter("file_hashes.txt")

    for database in databases:
        database_contents, file_identifier = DatabaseReader(database, hash_writer).get_database()
        if hash_writer.file_is_unique(file_identifier):
            try:
                combined_delimited_database = DatabaseCombiner(additional_information).combine(database_contents,
                                                                                               database)
                database_writer = JsonWriter(DatabaseCombiner.get_file_name(database), combined_delimited_database)
                database_writer.write_as_json()
                hash_writer.new_valid_hashes.append(file_identifier)
            except ValueError as e:
                hash_writer.new_invalid_hashes.append(file_identifier)
    hash_writer.write_hashes_to_file()
