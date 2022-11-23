from Connection.DatabaseConnection import DatabaseConnection
from main.usage import Usage

if __name__ == '__main__':
    collections = DatabaseConnection()
    hash_collection = collections.hash_collection
    data_collection = collections.data_collection
    database_collection = collections.database_collection

    Usage(hash_collection, data_collection, database_collection).run()
