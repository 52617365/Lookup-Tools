import pandas as pd

from Database.DatabaseCombiner import DatabaseCombiner
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

    for database in databases:
        try:
            combined_delimited_database = DatabaseCombiner(additional_information).combine(database)
        except Exception as e:
            # TODO: append to invalid hashes
            print(f"Failed to combine {database} with error: {e}")
