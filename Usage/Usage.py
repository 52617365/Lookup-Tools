import pandas as pd
from pandas import DataFrame

from Database.DatabaseCombiner import DatabaseCombiner
from DatabaseWriter.HashWriter import HashWriter
from DatabaseWriter.JsonWriter import JsonWriter
from FileGlob.FileGlob import FileGlob
from Format.Input import IDKException
from Reader.DatabaseReader import DatabaseReader, FileIsJunk
from Usage.UserArguments import CommandLineArguments


class Usage:
    def __init__(self, hash_collection, data_collection, database_collection):
        self.__user_arguments = CommandLineArguments().get()
        self.additional_information = self.__get_additional_information()
        self.hash_writer = HashWriter(hash_collection)
        self.__data_collection = data_collection
        self.__database_collection = database_collection

    def __get_additional_information(self):
        try:
            additional_information = pd.read_csv(self.__user_arguments.additional)
            return additional_information
        except OSError:
            quit(F"Additional information file not found at {self.__user_arguments.additional}")

    def run(self):
        database_paths = self.get_database_paths()
        for database_path in database_paths:
            self.handle_database(database_path)

    def get_database_paths(self):
        if self.__user_arguments.glob:
            databases = FileGlob(self.__user_arguments.input).get_files_from_directories()
        else:
            databases = [self.__user_arguments.input]
        return databases

    def handle_database(self, database_path):
        try:
            # TODO: 1. Check in chunks that the file is in correct format.
            # TODO: 2. If it is, then read the file in chunks and write to Mongo.
            database_contents, file_identifier = DatabaseReader(database_path,
                                                                self.__user_arguments.manual).get_database()
            combined_database_contents = self.__combine_additional_information_to_database(database_contents,
                                                                                           database_path)
            self.__write_file_to_database(combined_database_contents, file_identifier)

            database_name = combined_database_contents['database_name'].iloc[0]
            self.hash_writer.write_valid_hash(file_identifier, database_name)
        except IDKException:
            return
        except FileIsJunk:
            return

    def __combine_additional_information_to_database(self, database_contents: DataFrame, database_path: str):
        combined_delimited_database = DatabaseCombiner(self.additional_information)
        combined_database_contents = combined_delimited_database.combine(database_contents, database_path)
        return combined_database_contents

    def __write_file_to_database(self, combined_database_contents: DataFrame, file_identifier: str):
        database_writer = JsonWriter(combined_database_contents, self.__data_collection, self.__database_collection)

        if self.hash_writer.hash_is_unique(file_identifier):
            database_writer.insert_database_contents_as_json()
            database_writer.insert_database_additional_information()
