from datetime import datetime
from typing import Mapping, Any

import pandas as pd
from pymongo.collection import Collection


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
            database_name = self.__data_to_write['database_name'].iloc[0]
            lines_in_database = len(self.__data_to_write)
            breach_date = self.__data_to_write['breach_date'].iloc[0]
            if breach_date is None:
                self.mongo_databases_collection.insert_one(
                    {'database_name': database_name, 'lines_in_database': lines_in_database, 'added': datetime.now()})
            else:
                self.mongo_databases_collection.insert_one(
                    {'database_name': database_name, 'lines_in_database': lines_in_database, 'breach_date': breach_date,
                     'added': datetime.now()})
        except Exception as e:
            quit("There was an error while writing to MongoDB: " + str(e))
