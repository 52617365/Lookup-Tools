from dataclasses import dataclass
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
                 ):
        self.__combined_database_contents = combined_database_contents
        self.__data_collection = data_collection

    def insert_database_contents_as_json(self):
        try:
            if self.__combined_database_contents.empty:
                quit("The database is empty, so we will not write it to MongoDB.")
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
