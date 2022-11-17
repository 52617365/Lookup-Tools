import os
import warnings

import pandas as pd
from pandas import DataFrame
from pandas.errors import ParserWarning


class DatabaseReader:
    def __init__(self, database_file_path: str, additional_database_information: DataFrame):
        self.database_file_path = database_file_path
        self.additional_information = additional_database_information

    def get_database_as_dataframe(self) -> pd.DataFrame:
        csv_file: DataFrame = self.__get_csv_with_custom_delimiter_turning_warnings_into_errors()
        return csv_file

    def __get_csv_with_custom_delimiter_turning_warnings_into_errors(self) -> DataFrame:
        # Hack to turn warnings into errors.
        with warnings.catch_warnings():
            warnings.simplefilter("error", category=ParserWarning)
            csv_file = pd.read_csv(self.database_file_path, engine='python', sep=None,
                                   skipinitialspace=True,
                                   index_col=False)
            return csv_file

    def get_breach_date_from_additional_database_information(self) -> str | None:
        try:
            breach_date = self.additional_information.loc[
                self.additional_information['database'] == self.get_file_name(), 'dumped'].item()
            return breach_date
        except ValueError:
            return None

    def get_file_name(self) -> str:
        return os.path.splitext(os.path.basename(self.database_file_path))[0]
