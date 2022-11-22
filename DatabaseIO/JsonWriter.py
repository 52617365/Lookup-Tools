import pandas as pd

from Database.DatabaseCombiner import DatabaseCombiner


class JsonWriter:
    def __init__(self, database_file: str, data_to_write: pd.DataFrame):
        self.database_file_name = DatabaseCombiner.get_file_name(database_file)
        self.__data_to_write = data_to_write

    def write_as_json(self):
        try:
            self.__data_to_write.to_json(F"parsed/{self.__get_json_file_name()}", orient='records')
        except OSError:
            quit("Make sure the 'parsed' folder exists")

    def __get_json_file_name(self):
        return self.database_file_name + ".json"
