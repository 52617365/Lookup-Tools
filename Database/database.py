from pandas import DataFrame

from DatabaseFile.database_reader import DatabaseReader


class Database:
    """Initializing this class can possibly fail if the database format in invalid."""

    def __init__(self, path_to_database: str, additional_database_information: DataFrame):
        file_reader_to_database = DatabaseReader(path_to_database)
        self.__database_name = file_reader_to_database.file.get_file_name()
        self.__additional_information = additional_database_information
        self.__database_contents = file_reader_to_database.get_database_as_dataframe()

    def combine(self) -> DataFrame:
        database_contents_with_additional_information = self.__set_additional_information_to_database()
        return database_contents_with_additional_information

    def __set_additional_information_to_database(self):
        breach_date = self.__get_additional_information()

        database_contents_with_additional_information = self.__database_contents

        self.__set_db_name(database_contents_with_additional_information)
        self.__set_breach_date(breach_date, database_contents_with_additional_information)

        return database_contents_with_additional_information

    def __set_db_name(self, database_contents_with_additional_information):
        database_contents_with_additional_information["database_name"] = self.__database_name

    @staticmethod
    def __set_breach_date(breach_date: str, database_contents_with_additional_information: DataFrame):
        if breach_date is not None:
            database_contents_with_additional_information["breach_date"] = breach_date

    def __get_additional_information(self) -> str:
        breach_date = self.__get_breach_date_from_additional_database_information()
        return breach_date

    def __get_breach_date_from_additional_database_information(self) -> str | None:
        try:
            breach_date = self.__additional_information.loc[
                self.__additional_information['database'] == self.__database_name, 'dumped'].item()
            return breach_date
        except ValueError:
            return None
