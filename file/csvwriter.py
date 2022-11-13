import pandas as pd


class CsvWriter:
    def __init__(self, writing_file_path: str, data_to_write: pd.DataFrame):
        self.__path_to_writing_file = writing_file_path
        self.__data_to_write = data_to_write

    def write_as_json(self):
        self.__data_to_write.to_json(self.__path_to_writing_file, orient='records')

    def write_as_csv(self):
        self.__data_to_write.to_csv(self.__path_to_writing_file, index=False)
