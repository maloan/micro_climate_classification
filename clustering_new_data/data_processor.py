"""
This module contains the DataProcessor class,
which is used to process the data and create pivot tables.
"""
from asyncio.log import logger

import pandas as pd


class DataProcessor:
    """
    This class is used to process the data and create pivot tables.

    Args:
        data (DataFrame): The data to be processed.
        mode (str): The mode of the data, either 'radiation' or 'temperature'.

    Attributes:
        result_data_temperature (DataFrame): The processed temperature data.
        result_data_radiation (DataFrame): The processed radiation data.
    """

    def __init__(self, data, mode):
        self.data = data
        self.mode = mode
        self.result_data_temperature = None
        self.result_data_radiation = None
        self.process_data()

    def melt_data(self):
        """
        This function melts the data and creates a pivot table.

        Returns:
            DataFrame: The melted and pivoted data.
        """
        data, value_vars = self.prepare_data(self.data)
        id_vars = "radiation_category" if self.mode == "radiation" else "temperature_category"
        value_name = "solar_voltage" if self.mode == "radiation" else "temperature"
        merged_df = pd.melt(data, id_vars=[id_vars], value_vars=value_vars,
                            var_name="sensor", value_name=value_name)
        return self.create_melted_pivot_table(merged_df, id_vars, value_name)

    @staticmethod
    def create_melted_pivot_table(merged_df, id_vars, value_name):
        """
        This function creates a pivot table from the melted data.

        Args:
            merged_df (DataFrame): The melted data.
            id_vars (str): The list of ID variables.
            value_name (str): The name of the value variable.

        Returns:
            DataFrame: The pivoted data.
        """
        pivot_table = merged_df.pivot_table(
            index="sensor", columns=[id_vars],
            values=value_name, aggfunc=["mean"])
        pivot_table.columns = pivot_table.columns.droplevel(0)
        pivot_table.fillna(0, inplace=True)
        return pivot_table

    def prepare_data(self, data):
        """
        This function prepares the data for processing.

        Args:
            data (DataFrame): The data to be processed.

        Returns:
            DataFrame: The prepared data.
            list: The list of value variables.
        """
        if self.mode == "radiation":
            data = data.drop(columns=[col for col in data.columns if
                                      "temperature_boum" in col or "temperature_category" in col
                                      or "temperature_2m" in col])
            value_vars = data.columns.drop(["month", "radiation_category"])
        else:
            data = data.drop(columns=[col for col in data.columns if
                                      "solarVoltage_boum" in col or "radiation_category" in col
                                      or "direct_normal_irradiance" in col])
            value_vars = data.columns.drop(["month", "temperature_category"])
        return data, value_vars

    def process_data(self):
        """
        This function processes the data and stores the results.

        Returns:
            DataFrame or None: The processed data, depending on the mode.

        Raises:
            ValueError: If the data cannot be processed.
        """
        try:
            if self.mode == 'radiation':
                self.result_data_radiation = self.melt_data()
                if self.result_data_radiation.empty:
                    raise ValueError("Failed to process the radiation data.")
                return self.result_data_radiation
            self.result_data_temperature = self.melt_data()
            if self.result_data_temperature.empty:
                raise ValueError("Failed to process the temperature data.")
            return self.result_data_temperature

        except ValueError as value_error:
            logger.error("ValueError in processing data: %s", value_error)
            raise
        except Exception as exception:
            logger.error("Exception in processing data: %s", exception)
            raise
