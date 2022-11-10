from pandas import DataFrame

from file.csv import read_csv_file
from file.file import get_file_without_path_or_extension


class Database:
    def __init__(self, path_to_database, additional_database_information):
        self.__database_name = get_file_without_path_or_extension(path_to_database)
        try:
            self.__additional_information = read_csv_file(additional_database_information)
            self.__database_contents = read_csv_file(path_to_database)
        except Exception as e:
            raise e

    def combine(self) -> DataFrame:
        self.__set_additional_information_to_database()
        return self.__database_contents

    def get_database_name(self) -> str:
        return self.__database_name

    def get_database_contents(self) -> DataFrame:
        return self.__database_contents

    def get_additional_information(self) -> (str, str):
        breach_date = self.__get_breach_date_from_additional_database_information()
        database_name = self.get_database_name()
        return breach_date, database_name

    def __set_additional_information_to_database(self):
        breach_date, database_name = self.get_additional_information()
        self.__database_contents["database_name"] = database_name
        if breach_date is not None:
            self.__database_contents["breach_date"] = breach_date

    def __get_breach_date_from_additional_database_information(self):
        for index, row in self.__additional_information.iterrows():
            if row["database"] == self.__database_name:
                breach_date = row["dumped"]
                return breach_date
        return None


if __name__ == '__main__':
    try:
        database = Database("../000webhost.com.csv", "../list_of_leaks.txt")
        combined_database = database.combine()
        print(combined_database)
    except Exception as e:
        print(e)
