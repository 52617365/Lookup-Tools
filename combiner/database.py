from pandas import DataFrame

from file.file_reader import FileReader


class Database:
    def __init__(self, path_to_database: str, additional_database_information: DataFrame):
        self.__file = FileReader(path_to_database)
        self.__database_name = self.__file.get_file_name()
        self.__additional_information = additional_database_information
        self.__database_contents = self.__file.get_file_as_dataframe()

    def combine(self) -> DataFrame:
        self.__set_additional_information_to_database()
        return self.__database_contents

    def get_additional_information(self) -> str:
        breach_date = self.__get_breach_date_from_additional_database_information()
        return breach_date

    def __set_additional_information_to_database(self):
        breach_date = self.get_additional_information()
        self.__database_contents["database_name"] = self.__database_name
        if breach_date is not None:
            self.__database_contents["breach_date"] = breach_date

    def __get_breach_date_from_additional_database_information(self) -> str | None:
        try:
            breach_date = self.__additional_information.loc[
                self.__additional_information['database'] == self.__database_name, 'dumped'].item()
            return breach_date
        except ValueError:
            return None
