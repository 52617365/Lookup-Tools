from typing import Mapping, Any

import pandas as pd
from pymongo.collection import Collection


class JsonWriter:
    def __init__(self, data_to_write: pd.DataFrame, mongo_collection: Collection[Mapping[str, Any]]):
        self.__data_to_write = data_to_write
        self.mongo_collection = mongo_collection

    def write_as_json(self):
        try:
            data_to_write_in_json = self.__data_to_write.to_dict(orient='records')
            self.mongo_collection.insert_many(data_to_write_in_json)
        except Exception as e:
            quit("There was an error while writing to MongoDB: " + str(e))
