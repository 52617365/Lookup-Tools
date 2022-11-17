from Database.DatabaseCombiner import DatabaseCombiner
from FileGlob.FileGlob import FileGlob
from main.UserArguments import CommandLineArguments

if __name__ == '__main__':
    args = CommandLineArguments().get()
    if args.glob:
        databases = FileGlob(args.input).get_files_from_directories()
    else:
        databases = [args.input]

    for database in databases:
        try:
            combiner = DatabaseCombiner(database, args.additional)
            combined_delimited_database = combiner.set_additional_information_to_database()
        except Exception as e:
            # TODO: append to invalid hashes
            print(f"Failed to combine {database} with error: {e}")
