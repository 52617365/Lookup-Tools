import pandas as pd

from file.filereader import FileReader


class CsvWriter:
    def __init__(self, writing_file_path: str, data_to_write: pd.DataFrame):
        self.__path_to_writing_file = writing_file_path
        self.__data_to_write = data_to_write

    def write_as_json(self):
        # TODO: maybe add some folder to write to instead to keep stuff organized?
        data_in_json = self.__data_to_write.to_json(self.__path_to_writing_file, orient='records')

    def write(self):
        # TODO: maybe add some folder to write to instead to keep stuff organized?
        self.__data_to_write.to_csv(self.__path_to_writing_file, index=False)


if __name__ == '__main__':
    file = FileReader("../000webhost.com.csv")
    data = file.get_file_as_csv()
    writer = CsvWriter("test.json", data)
    writer.write_as_json()
