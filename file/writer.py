import pandas as pd


class Writer:
    def __init__(self, writing_file_path: str, data_to_write: pd.DataFrame):
        self.__path_to_writing_file = writing_file_path
        self.__data_to_write = data_to_write

    def write_as_json(self):
        # TODO: maybe add some folder to write to instead to keep stuff organized?
        data_in_json = self.__data_to_write.to_json(self.__path_to_writing_file)

    def write_as_csv(self):
        # TODO: maybe add some folder to write to instead to keep stuff organized?
        data_in_csv = self.__data_to_write.to_csv(self.__path_to_writing_file)
