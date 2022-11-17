from pandas import DataFrame

from DatabaseIO.DatabaseReader import DatabaseReader


class DatabaseCombiner:
    def __init__(self, database_file_path: str, additional_database_information: DataFrame):
        self.reader = DatabaseReader(database_file_path, additional_database_information)
        self.breach_date = self.reader.get_breach_date_from_additional_database_information()
        self.database_contents_with_additional_information = self.reader.get_database_as_dataframe()

    def set_additional_information_to_database(self):
        self.__set_db_name()
        self.__set_breach_date()

        return self.database_contents_with_additional_information

    def __set_db_name(self):
        self.database_contents_with_additional_information["database_name"] = self.reader.get_file_name()

    def __set_breach_date(self):
        if self.breach_date is not None:
            self.database_contents_with_additional_information["breach_date"] = self.breach_date
