import pandas as pd
from pandas import DataFrame

from Database.DatabaseCombiner import DatabaseCombiner
from DatabaseIO.DatabaseReader import DatabaseReader
from DatabaseIO.HashWriter import HashWriter
from DatabaseIO.JsonWriter import JsonWriter
from FileGlob.FileGlob import FileGlob
from main.UserArguments import CommandLineArguments


class Usage:
    def __init__(self):
        self.__user_arguments = CommandLineArguments().get()
        self.hash_writer = HashWriter("file_hashes.txt")
        self.additional_information = self.get_additional_information()

    def get_additional_information(self):
        try:
            additional_information = pd.read_csv(self.__user_arguments.additional)
            return additional_information
        except OSError:
            quit("Additional information file not found")

    def run(self):
        database_paths = self.get_database_paths()
        for database_path in database_paths:
            try:
                self.handle_database(database_path)
            except ValueError:
                continue
        self.hash_writer.write_hashes_to_file()

    def get_database_paths(self):
        if self.__user_arguments.glob:
            databases = FileGlob(self.__user_arguments.input).get_files_from_directories()
        else:
            databases = [self.__user_arguments.input]
        return databases

    def handle_database(self, database_path):
        global file_identifier
        try:
            database_contents, file_identifier = self.__read_database(database_path)
            combined_database_contents = self.__combine_additional_information_to_database(database_contents,
                                                                                           database_path)
            self.__write_file_as_json(database_path, combined_database_contents)
            self.hash_writer.new_valid_hashes.add(file_identifier)
        except ValueError:
            self.hash_writer.new_invalid_hashes.add(file_identifier)

    def __read_database(self, database_path):
        database_contents, file_identifier = DatabaseReader(database_path, self.hash_writer).get_database()
        return database_contents, file_identifier

    def __combine_additional_information_to_database(self, database_contents: DataFrame, database_path: str):
        combined_delimited_database = DatabaseCombiner(self.additional_information)
        combined_database_contents = combined_delimited_database.combine(database_contents, database_path)
        return combined_database_contents

    @staticmethod
    def __write_file_as_json(database_path: str, combined_database_contents: DataFrame):
        database_writer = JsonWriter(DatabaseCombiner.get_file_name(database_path), combined_database_contents)
        database_writer.write_as_json()


# TODO: We are currently not checking for if the file is invalid, fix this.

if __name__ == '__main__':
    Usage().run()
