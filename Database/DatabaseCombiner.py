import os

import pandas as pd
from pandas import DataFrame

from DatabaseIO.DatabaseReader import DatabaseReader


class DatabaseCombiner:
    def __init__(self, additional_database_information: DataFrame):
        self.additional_database_information = additional_database_information

    def combine(self, database_file_path: str) -> pd.DataFrame:
        reader = DatabaseReader(database_file_path, self.additional_database_information)

        database = reader.get_database_as_dataframe()

        self.__set_db_name(database, database_file_path)
        self.__set_breach_date(database, database_file_path)

        return database

    def __set_db_name(self, database: DataFrame, database_file_path: str):
        database_name = self.get_file_name(database_file_path)
        database["database_name"] = database_name

    def __set_breach_date(self, database: DataFrame, database_file_path: str):
        breach_date = self.get_breach_date_from_additional_database_information(database_file_path)
        if breach_date is not None:
            database["breach_date"] = breach_date

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
