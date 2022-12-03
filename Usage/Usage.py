import pandas as pd
from pandas import DataFrame
from pandas.errors import ParserError, ParserWarning

from Database.DatabaseCombiner import DatabaseCombiner
from DatabaseWriter.HashWriter import HashWriter
from DatabaseWriter.JsonWriter import JsonWriter
from FileGlob.FileGlob import FileGlob
from Reader.DatabaseReader import DatabaseReader, WeWantToSkipFile
from Reader.Hash import Hash
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
        # TODO: make sure the file is in a correct format here or something.
        try:
            file_identifier = Hash.get_hash_from_file_contents(database_path)

            reader = DatabaseReader(database_path,
                                    self.__user_arguments.manual)
            database_content_chunks = reader.get_database_chunks()

            for chunk in database_content_chunks:
                self.handle_chunk(chunk, database_path, file_identifier)
        except WeWantToSkipFile as e:
            print(e)
            return

    def handle_chunk(self, chunk, database_path, file_identifier):
        try:
            combined_database_contents = self.__combine_additional_information_to_database(chunk,
                                                                                           database_path)
            self.__write_file_to_mongo_database(combined_database_contents, file_identifier)

            database_name = combined_database_contents['database_name'].iloc[0]
            self.hash_writer.write_valid_hash(file_identifier, database_name)
        except ParserError:
            quit(F"The file does not have a valid format.")
        except ParserWarning:
            quit(F"The file does not have a valid format.")

    def __combine_additional_information_to_database(self, database_contents: DataFrame, database_path: str):
        combined_delimited_database = DatabaseCombiner(self.additional_information)
        combined_database_contents = combined_delimited_database.combine(database_contents, database_path)
        return combined_database_contents

    def __write_file_to_mongo_database(self, combined_database_contents: DataFrame, file_identifier: str):
        database_writer = JsonWriter(combined_database_contents, self.__data_collection, self.__database_collection)

        if self.hash_writer.hash_is_unique(file_identifier):
            database_writer.insert_database_contents_as_json()
            database_writer.insert_database_additional_information()
