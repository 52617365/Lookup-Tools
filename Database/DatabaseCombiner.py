import os

from pandas import DataFrame


class DatabaseCombiner:
    def __init__(self, additional_database_information: DataFrame):
        self.additional_database_information = additional_database_information

    def combine(self, database_contents: DataFrame, database_file_path: str) -> DataFrame:
        self.__set_db_name(database_contents, database_file_path)
        self.__set_breach_date(database_contents, database_file_path)
        return database_contents

    def __set_db_name(self, database_contents: DataFrame, database_file_path: str):
        database_name = self.get_file_name(database_file_path)
        database_contents["database_name"] = database_name

    def __set_breach_date(self, database_contents: DataFrame, database_file_path: str):
        breach_date = self.get_breach_date_from_additional_database_information(database_file_path)
        if breach_date is not None:
            database_contents["breach_date"] = breach_date

    def get_breach_date_from_additional_database_information(self, database_file_path: str) -> str | None:
        try:
            breach_date = self.additional_database_information.loc[
                self.additional_database_information['database'] == self.get_file_name(
                    database_file_path), 'dumped'].item()
            return breach_date
        except ValueError:
            return None

    @staticmethod
    def get_file_name(database_file_path: str) -> str:
        return os.path.splitext(os.path.basename(database_file_path))[0]
