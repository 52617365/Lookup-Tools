import sys

import pandas as pd

from file.filereader import FileReader


class CsvWriter:
    def __init__(self, writing_file_path: str, data_to_write: pd.DataFrame | str):
        self.__path_to_writing_file = writing_file_path
        self.__data_to_write = data_to_write

    def write_as_json(self):
        if isinstance(self.__data_to_write, pd.DataFrame):
            self.__data_to_write.to_json(self.__path_to_writing_file, orient='records')
        else:
            print("This function can only be called with dataframes.")
            sys.exit(1)

    def write_as_csv(self):
        if isinstance(self.__data_to_write, pd.DataFrame):
            self.__data_to_write.to_csv(self.__path_to_writing_file, index=False)
        else:
            print("This function can only be called with dataframes.")
            sys.exit(1)

    def write_hash_to_file(self):
        if isinstance(self.__data_to_write, str):
            with open(self.__path_to_writing_file, 'a') as hashes_file:
                hashes_file.write(self.__data_to_write + "\n")
        else:
            print("This function can only be called with strings containing hashes.")
            sys.exit(1)


if __name__ == '__main__':
    file = FileReader("../000webhost.com.csv")
    data = file.get_file_as_dataframe()
    print(data)
    writer = CsvWriter("test.json", data)
    writer.write_as_json()
