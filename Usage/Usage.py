import pandas as pd
from pandas import DataFrame

from Database.DatabaseCombiner import DatabaseCombiner
from DatabaseWriter.AdditionalWriter import AdditionalWriter
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
        self.__additional_writer = AdditionalWriter(database_collection)

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
            reader = DatabaseReader(database_path,
                                    self.__user_arguments.manual, self.__user_arguments.skip_invalid_lines)
            self.handle_chunks(database_path, reader)
        except WeWantToSkipFile as e:
            print(e)
            return

    def handle_chunks(self, database_path, reader: DatabaseReader):
        file_identifier = Hash.get_hash_from_file_contents(database_path)
        if self.hash_writer.hash_is_unique(file_identifier):
            self.validate_file_if_user_wanted_to(reader)

            lines_in_database = 0

            database_chunk_generator = reader.get_json_or_csv_database_chunk_iterator()
            for chunk in database_chunk_generator:
                lines_in_database += len(chunk)

                combined_database_contents = self.__combine_additional_information_to_database(chunk,
                                                                                               database_path)
                self.__write_file_to_mongo_database(combined_database_contents, file_identifier)

            self.hash_writer.write_valid_hash(file_identifier, database_path)
            self.__additional_writer.insert_database_additional_information(database_path, lines_in_database,
                                                                            self.additional_information)

    def validate_file_if_user_wanted_to(self, reader):
        if self.__user_arguments.skip_invalid_lines:
            print(
                "Not validating format because you used the specified so in the -s flag, instead we skip bad lines.")
        else:
            self.validate_database(reader)

    @staticmethod
    def validate_database(reader):
        # Creating a new iterator to avoid having to implement a hack to "reset" the iterator back to start once it's exhausted.
        iterator_to_check_database_format = reader.get_json_or_csv_database_chunk_iterator()
        reader.terminate_if_csv_database_invalid_format(iterator_to_check_database_format)

    def __combine_additional_information_to_database(self, database_contents: DataFrame, database_path: str):
        combined_delimited_database = DatabaseCombiner(self.additional_information)
        combined_database_contents = combined_delimited_database.combine(database_contents, database_path)
        return combined_database_contents

    def __write_file_to_mongo_database(self, combined_database_contents: DataFrame, file_identifier: str):
        database_writer = JsonWriter(combined_database_contents, self.__data_collection)

        if self.hash_writer.hash_is_unique(file_identifier):
            database_writer.insert_database_contents_as_json()
