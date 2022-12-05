from datetime import datetime

from Database.DatabaseCombiner import get_file_name_from_path, get_breach_date_from_additional_database_information


class AdditionalWriter:
    def __init__(self, database_collection):
        self.__database_collection = database_collection

    def insert_database_additional_information(self, database_path: str, lines_in_database: int,
                                               additional_information):
        database_name = get_file_name_from_path(database_path)
        breach_date = get_breach_date_from_additional_database_information(database_path, additional_information)
        try:
            if breach_date is None:
                self.__insert_information_without_breach_date(database_name, lines_in_database)
            else:
                self.__insert_information_with_breach_date(database_name, lines_in_database, breach_date)
        except Exception as e:
            quit("There was an error while writing to MongoDB: " + str(e))

    def __insert_information_without_breach_date(self, database_name, lines_in_database):
        self.__database_collection.insert_one(
            {'database_name': database_name,
             'lines_in_database': lines_in_database,
             'added': datetime.now()})

    def __insert_information_with_breach_date(self, database_name, lines_in_database, breach_date):
        self.__database_collection.insert_one(
            {'database_name': database_name,
             'lines_in_database': lines_in_database,
             'breach_date': breach_date,
             'added': datetime.now()})
