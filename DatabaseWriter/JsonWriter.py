from dataclasses import dataclass
from datetime import datetime
from typing import Mapping, Any

import numpy as np
import pandas as pd
from pymongo.collection import Collection


@dataclass
class DatabaseInformation:
    database_name: str
    lines_in_database: int
    breach_date: str | None


class JsonWriter:
    def __init__(self, combined_database_contents: pd.DataFrame,
                 data_collection: Collection[Mapping[str, Any]] | None,
                 database_collection: Collection[Mapping[str, Any]] | None):
        self.__combined_database_contents = combined_database_contents
        self.__data_collection = data_collection
        self.__database_collection = database_collection

    def insert_database_contents_as_json(self):
        try:
            data_to_write_in_json = self.__combined_database_contents.to_dict(orient='records')
            self.delete_nan_values(data_to_write_in_json)
            self.__data_collection.insert_many(data_to_write_in_json)
        except Exception as e:
            quit("There was an error while writing to MongoDB: " + str(e))

    @staticmethod
    def delete_nan_values(data_to_write_in_json: list[dict]):
        for data in data_to_write_in_json:
            data_keys = [key for key in data]
            for key in data_keys:
                if data[key] is np.NaN:
                    del data[key]

    def insert_database_additional_information(self):
        try:
            database_information = self.__get_information_about_database()
            if database_information.breach_date is None:
                self.__insert_information_without_breach_date(database_information)
            else:
                self.__insert_information_with_breach_date(database_information)
        except Exception as e:
            quit("There was an error while writing to MongoDB: " + str(e))

    def __get_information_about_database(self) -> DatabaseInformation:
        database_name = self.__combined_database_contents['database_name'].iloc[0]
        lines_in_database = len(self.__combined_database_contents)
        breach_date = self.__combined_database_contents.get("breach_date", None)
        if breach_date is None:
            return DatabaseInformation(database_name, lines_in_database, None)
        else:
            return DatabaseInformation(database_name, lines_in_database, breach_date.iloc[0])

    def __insert_information_without_breach_date(self, database_information):
        self.__database_collection.insert_one(
            {'database_name': database_information.database_name,
             'lines_in_database': database_information.lines_in_database,
             'added': datetime.now()})

    def __insert_information_with_breach_date(self, database_information):
        self.__database_collection.insert_one(
            {'database_name': database_information.database_name,
             'lines_in_database': database_information.lines_in_database,
             'breach_date': database_information.breach_date,
             'added': datetime.now()})
