import pandas as pd


class JsonWriter:
    def __init__(self, database_file_name: str, data_to_write: pd.DataFrame):
        self.database_file_name = database_file_name
        self.__data_to_write = data_to_write

    def write_as_json(self):
        self.__data_to_write.to_json(self.get_json_file_name(), orient='records')

    def get_json_file_name(self):
        return self.database_file_name + ".json"
