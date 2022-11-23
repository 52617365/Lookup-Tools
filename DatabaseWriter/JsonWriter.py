from dataclasses import dataclass
from datetime import datetime
from typing import Mapping, Any

import pandas as pd
from pymongo.collection import Collection


@dataclass
class DatabaseInformation:
    database_name: str
    lines_in_database: int
    breach_date: str | None


class JsonWriter:
    def __init__(self, data_to_write: pd.DataFrame, mongo_data_collection: Collection[Mapping[str, Any]] | None,
                 mongo_databases_collection: Collection[Mapping[str, Any]] | None):
        self.__data_to_write = data_to_write
        self.mongo_data_collection = mongo_data_collection
        self.mongo_databases_collection = mongo_databases_collection

    def write_as_json(self):
        try:
            data_to_write_in_json = self.__data_to_write.to_dict(orient='records')
            self.mongo_data_collection.insert_many(data_to_write_in_json)
        except Exception as e:
            quit("There was an error while writing to MongoDB: " + str(e))

    def write_additional_information(self):
        try:
            database_information = self.__get_information_about_database()
            if database_information.breach_date is None:
                self.__insert_information_without_breach_date(database_information)
            else:
                self.__insert_information_with_breach_date(database_information)
        except Exception as e:
            quit("There was an error while writing to MongoDB: " + str(e))

    def __get_information_about_database(self) -> DatabaseInformation:
        database_name = self.__data_to_write['database_name'].iloc[0]
        lines_in_database = len(self.__data_to_write)
        breach_date = self.__data_to_write['breach_date'].iloc[0]
        return DatabaseInformation(database_name, lines_in_database, breach_date)

    def __insert_information_without_breach_date(self, database_information):
        self.mongo_databases_collection.insert_one(
            {'database_name': database_information.database_name,
             'lines_in_database': database_information.lines_in_database,
             'added': datetime.now()})

    def __insert_information_with_breach_date(self, database_information):
        self.mongo_databases_collection.insert_one(
            {'database_name': database_information.database_name,
             'lines_in_database': database_information.lines_in_database,
             'breach_date': database_information.breach_date,
             'added': datetime.now()})
