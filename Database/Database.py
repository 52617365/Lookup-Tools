from pandas import DataFrame

from DatabaseIO.DatabaseReader import DatabaseReader


class Database:
    """Initializing this class can possibly fail if the database format in invalid."""

    def __init__(self, database_path: str, additional_database_information: DataFrame):
        self.reader = DatabaseReader(database_path)
        self.__additional_information = additional_database_information

    def set_additional_information_to_database(self):
        breach_date = self.__get_breach_date_from_additional_database_information()

        database_contents_with_additional_information = self.reader.get_database_as_dataframe()

        self.__set_db_name(database_contents_with_additional_information)
        self.__set_breach_date(breach_date, database_contents_with_additional_information)

        return database_contents_with_additional_information

    def __get_breach_date_from_additional_database_information(self) -> str | None:
        try:
            breach_date = self.__additional_information.loc[
                self.__additional_information['database'] == self.reader.get_file_name(), 'dumped'].item()
            return breach_date
        except ValueError:
            return None

    def __set_db_name(self, database_contents_with_additional_information):
        database_contents_with_additional_information["database_name"] = self.reader.get_file_name()

    @staticmethod
    def __set_breach_date(breach_date: str, database_contents_with_additional_information: DataFrame):
        if breach_date is not None:
            database_contents_with_additional_information["breach_date"] = breach_date
