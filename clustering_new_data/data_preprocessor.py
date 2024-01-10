"""
This module contains the functions to preprocess the given data.
"""
import gc

import numpy as np
import pandas as pd

from clustering_new_data.config import (MAX_TIME, MIN_TIME, VOLTAGE_THRESHOLD,
                                        RADIATION_THRESHOLDS, TEMPERATURE_THRESHOLDS,
                                        TEMP_CORRECTION_COEFFICIENT, TEMP_CORRECTION_INTERCEPT)
from msc.MathClass import interpolate_dataframe_to_resolution


class DataPreprocessor:
    """
    This class is responsible for preprocessing the data before clustering.
    It takes in the BOUM data and weather data, along with the month and the device ID,
    and preprocesses the data to prepare it for clustering.

    Attributes:
        processed_data (DataFrame): The preprocessed data.
        boum_data (DataFrame): The BOUM data.
        weather_data (DataFrame): The weather data.
        target_month (int): The month for which the data is being processed.
        device_id (str): The device ID.
        config_data (dict): The configuration data.
    """

    def __init__(self, boum_data, weather_data, target_month, device_id):
        """
        Initialize the DataPreprocessor class.
        """
        self.processed_data = None
        self.boum_data = boum_data
        self.weather_data = weather_data
        self.target_month = target_month
        self.device_id = device_id[:8]
        self.config_data = self.get_config_data()
        self.preprocess_data()

    @staticmethod
    def get_config_data():
        """
        This function returns the configuration data.

        Returns:
            dict: The configuration data.
        """
        return {'max_time': MAX_TIME, 'min_time': MIN_TIME,
                'radiation_thresholds': RADIATION_THRESHOLDS,
                'temperature_thresholds': TEMPERATURE_THRESHOLDS,
                'temp_offset': TEMP_CORRECTION_INTERCEPT,
                'temp_correction_factor': TEMP_CORRECTION_COEFFICIENT,
                'voltage_threshold': VOLTAGE_THRESHOLD}

    def preprocess_timestamps(self):
        """
        This function preprocesses the timestamps in the BOUM data.
        It attempts to convert the timestamps to datetime objects, remove the time zone information,
        convert the timestamps to milliseconds, and then resample the data to a 10-minute interval.

        Returns:
            DataFrame: The processed BOUM data, or None if an error occurred.

        Raises:
            ValueError: If an error occurs while preparing the timestamps.
        """
        try:
            self.boum_data['timestamp'] = pd.to_datetime(
                self.boum_data['timestamp']).dt.tz_localize(None)
            self.boum_data['timestamp'] = self.boum_data['timestamp'].values.astype(
                np.int64) // 10 ** 6 // 1000
            boum_data = interpolate_dataframe_to_resolution(
                self.boum_data, 'timestamp',
                600, self.boum_data.columns,
                "values")
            boum_data['timestamp'] = pd.to_datetime(boum_data['timestamp'], unit='s')
            boum_data.set_index('timestamp', inplace=True)
            return boum_data
        except ValueError as value_error:
            print(f"Error preprocessing timestamps: {value_error}")
            return None

    def correct_data(self):
        """
        This function corrects the data in the BOUM data.
        It attempts to convert the timestamps to datetime objects,
        convert the data to numeric values,
        apply the temperature correction factor and offset,
        and resample the data to a 30-minute interval.
        It also filters out any data points with a solar voltage above the voltage threshold.

        Returns:
            DataFrame: The corrected BOUM data, or None if an error occurred.
        """
        if "timestamp" in self.boum_data.columns:
            self.boum_data["timestamp"] = pd.to_datetime(self.boum_data["timestamp"])
            self.boum_data.set_index("timestamp", inplace=True)
        temperature_columns = [col for col in self.boum_data.columns
                               if col.startswith("temperature_boum")]
        voltage_columns = [col.replace("temperature", "solarVoltage")
                           for col in temperature_columns]
        self.boum_data = self.boum_data[temperature_columns + voltage_columns].apply(
            pd.to_numeric, errors="coerce")
        self.boum_data[voltage_columns] = self.boum_data[voltage_columns][
            self.boum_data[voltage_columns] <= self.config_data.get('voltage_threshold')]
        self.boum_data[temperature_columns] = (
                self.config_data.get('temp_correction_factor') *
                self.boum_data[temperature_columns] +
                self.config_data.get('temp_offset'))
        self.boum_data[temperature_columns + voltage_columns] = self.boum_data[
            temperature_columns + voltage_columns].mask(
            self.boum_data[temperature_columns + voltage_columns].diff().round(2) == 0)
        self.boum_data = self.boum_data.resample("30T").mean().dropna(how="all")
        return self.boum_data

    def extract_columns(self):
        """
        This function extracts the relevant columns from the BOUM data.
        It filters the columns based on the column names and returns a list of
        the temperature columns and a list of the voltage columns.

        Returns:
            tuple: A tuple containing the temperature columns and the voltage columns.
        """
        temperature_columns = self.boum_data.filter(like='temperature_boum').columns.tolist()
        voltage_columns = [col.replace("temperature", "solarVoltage")
                           for col in temperature_columns]
        return temperature_columns, voltage_columns

    def rename_columns(self):
        """
        This function renames the columns in the BOUM and weather data.
        It adds a month column to the BOUM data based on the index,
        and it sets the month column in the weather data as an integer.

        Returns:
            tuple: A tuple containing the processed BOUM data and the processed weather data.
        """
        if 'timestamp' in self.boum_data.columns:
            self.boum_data.set_index('timestamp', inplace=True)
        self.boum_data["m"] = self.boum_data.index.month
        self.boum_data["month"] = self.boum_data.index.strftime("%m-%d")
        self.boum_data.reset_index(inplace=True)
        if 'timestamp' in self.weather_data.columns:
            self.weather_data.set_index('timestamp', inplace=True)
        self.weather_data["month"] = self.weather_data.index.month
        return self.boum_data, self.weather_data

    def get_column_names(self):
        """
        This function returns the column names for the processed data.
        It concatenates the device ID to the temperature and voltage column names.

        Returns:
            tuple: A tuple containing the column names for the processed data.
        """
        return (f"temperature_2m_{self.device_id}", f"temperature_boum_{self.device_id}",
                f"solarVoltage_boum_{self.device_id}", f"direct_normal_irradiance_{self.device_id}")

    def sample_daily_mean(self, radiation_column, temperature_column):
        """
        This function samples the daily mean of
        the radiation and temperature data for the specified month.
        It resamples the data to a daily interval and returns the sampled data.

        Args:
            radiation_column (str): The radiation column name.
            temperature_column (str): The temperature column name.

        Returns:
            tuple: A tuple containing the sampled radiation data
            and the sampled temperature data.
        """
        seasonal_data = self.weather_data[self.weather_data["month"] == self.target_month].copy()
        seasonal_data.drop(
            columns=[col for col in seasonal_data.columns if "time" in col], inplace=True)
        temperature_data = seasonal_data[temperature_column].resample("D").mean()
        radiation_data = seasonal_data[radiation_column].resample("D").mean()
        temperature_categories = np.digitize(
            temperature_data, self.config_data.get('temperature_thresholds')[self.target_month - 1],
            right=True)
        radiation_categories = np.digitize(
            radiation_data, self.config_data.get('radiation_thresholds')[self.target_month - 1],
            right=True)
        temperature_data = pd.DataFrame(temperature_data)
        radiation_data = pd.DataFrame(radiation_data)
        temperature_data["temperature_category"] = temperature_categories
        radiation_data["radiation_category"] = radiation_categories
        temperature_data["month"] = temperature_data.index.month
        radiation_data["month"] = radiation_data.index.month
        return radiation_data, temperature_data

    def extract_data(self, value_column, data_value):
        """
        This function extracts the specified data from
        the BOUM data and merges it with the specified data.

        Args:
            value_column (str): The column name of the data to extract from the BOUM data.
            data_value (DataFrame): The data to merge with the extracted data.

        Returns:
            DataFrame: The merged data, or an empty DataFrame if an error occurred.

        Raises:
            pd.errors.EmptyDataError: Raised when the input data is empty.
            KeyError: Raised when the input data does not contain the specified column.
            ValueError: Raised when the input data contains invalid data.
        """
        try:
            extracted_data = self.boum_data[[value_column, "timestamp"]].copy()
            extracted_data['hour'] = pd.to_datetime(extracted_data['timestamp']).dt.hour
            extracted_data = extracted_data[extracted_data['hour'].between(
                self.config_data.get('min_time'), self.config_data.get('max_time'))]
            extracted_data.set_index('timestamp', inplace=True)
            extracted_data = extracted_data.resample('D').median()
            return pd.merge_ordered(extracted_data, data_value, on=['timestamp'], how='outer')
        except pd.errors.EmptyDataError:
            print("Empty data error in extract_data")
        except KeyError as key_error:
            print(f"Key error in extract_data: {key_error}")
        except ValueError as value_error:
            print(f"Value error in extract_data: {value_error}")

        return pd.DataFrame()

    @staticmethod
    def create_pivot_table(data: pd.DataFrame,
                           category_column: list,
                           value_column: str) -> pd.DataFrame:
        """
        This function creates a pivot table from the input data.

        Args:
            data (pd.DataFrame): The input data.
            category_column (list): The name of the column that contains the categories.
            value_column (str): The name of the column that contains the values to be aggregated.

        Returns:
            pd.DataFrame: The pivot table.
        """
        return data.groupby(
            category_column)[value_column].mean(
        ).reset_index(
        ).pivot_table(
            index=category_column,
            values=value_column,
            aggfunc="mean")

    @staticmethod
    def append_to_final(solar_pivot: pd.DataFrame,
                        temperature_pivot: pd.DataFrame, radiation_pivot: pd.DataFrame,
                        temp_pivot: pd.DataFrame) -> pd.DataFrame:
        """
        This function appends the solar, temperature, radiation,
        and temp_pivot dataframes to the final_data dataframe.
        If the final_data dataframe is empty,
        it will create a new dataframe with the concatenated dataframes.
        If the final_data dataframe is not empty,
        it will concatenate the new dataframes with the existing dataframe.

        Args:
            solar_pivot (pd.DataFrame): The solar pivot dataframe.
            temperature_pivot (pd.DataFrame): The temperature pivot dataframe.
            radiation_pivot (pd.DataFrame): The radiation pivot dataframe.
            temp_pivot (pd.DataFrame): The temp_pivot dataframe.

        Returns:
            pd.DataFrame: The final dataframe with the appended data.
        """
        final_data = pd.DataFrame()
        if final_data.empty:
            final_data = temp_pivot.join(radiation_pivot).join(
                temperature_pivot).join(solar_pivot)
        else:
            final_data = final_data.join(temp_pivot).join(
                radiation_pivot).join(temperature_pivot).join(
                solar_pivot)
        return final_data

    def preprocess_data_for_clustering(self):
        """
        This function prepares the data for clustering.
        It extracts the relevant columns from the BOUM and weather data,
        corrects the data, samples the daily average, and creates pivot tables.
        It then appends the pivot tables to a final dataframe and returns the resulting data.

        Returns:
            DataFrame: The processed data, or an empty DataFrame if an error occurred.

        Raises:
            pd.errors.EmptyDataError: Raised when the input data is empty.
            KeyError: Raised when the input data does not contain the specified column.
            ValueError: Raised when the input data contains invalid data.
            MemoryError: Raised when there is not enough memory to process the data.
        """
        resulting_data = pd.DataFrame()
        try:
            (pivot_boum_solar, pivot_boum_temperature,
             pivot_radiation, pivot_temperature) = self.create_sampled_data_tables()
            resulting_data = self.append_to_final(pivot_boum_solar,
                                                  pivot_boum_temperature,
                                                  pivot_radiation, pivot_temperature)
        except pd.errors.EmptyDataError:
            print(f"Empty data error occurred for BOUM ID {self.device_id}")
        except KeyError as key_error:
            print(f"Key error in data processing for BOUM ID {self.device_id}: {key_error}")
        except ValueError as value_error:
            print(f"Value error in data processing for BOUM ID {self.device_id}: {value_error}")
        except MemoryError as memory_error:
            print(f"Memory error in data processing for BOUM ID {self.device_id}: {memory_error}")
        gc.collect()
        return resulting_data

    def create_sampled_data_tables(self):
        """
        This function creates pivot tables from the input data and samples the daily means.

        Returns:
            tuple: A tuple containing the pivot tables for the BOUM solar and temperature data,
            the radiation data, and the temperature data.
        """
        (temperature_column, boum_temperature_column,
         boum_solar_column, radiation_column) = self.get_column_names()
        (boum_solar_data, boum_temperature_data,
         weather_radiation_data, weather_temperature_data) = self.extract_sampled_data(
            boum_solar_column, boum_temperature_column, radiation_column, temperature_column)
        pivot_boum_temperature = self.create_pivot_table(boum_temperature_data,
                                                         ["temperature_category"],
                                                         boum_temperature_column)
        pivot_boum_solar = self.create_pivot_table(boum_solar_data,
                                                   ['radiation_category'],
                                                   boum_solar_column)
        pivot_radiation = self.create_pivot_table(weather_radiation_data,
                                                  ["radiation_category", "month"],
                                                  radiation_column)
        pivot_temperature = self.create_pivot_table(weather_temperature_data,
                                                    ["temperature_category", "month"],
                                                    temperature_column)
        return pivot_boum_solar, pivot_boum_temperature, pivot_radiation, pivot_temperature

    def extract_sampled_data(self, boum_solar_column, boum_temperature_column,
                             radiation_column, temperature_column):
        """
        This function extracts the specified data from
        the BOUM data and merges it with the specified data.

        Args:
            boum_solar_column (str): The solar voltage column name in the BOUM data.
            boum_temperature_column (str): The temperature column name in the BOUM data.
            radiation_column (str): The radiation column name in the weather data.
            temperature_column (str): The temperature column name in the weather data.

        Returns:
            tuple: A tuple containing the BOUM solar data,
            the BOUM temperature data, the weather radiation data, and the weather temperature data.

        Raises:
            ValueError: If an error occurs while extracting the data.
        """
        try:
            weather_radiation_data, weather_temperature_data = self.sample_daily_mean(
                radiation_column,
                temperature_column)
            boum_temperature_data = self.extract_data(boum_temperature_column,
                                                      weather_temperature_data)
            boum_solar_data = self.extract_data(boum_solar_column, weather_radiation_data)
            return (boum_solar_data, boum_temperature_data,
                    weather_radiation_data, weather_temperature_data)
        except ValueError as value_error:
            print(f"Error occurred while extracting data: {value_error}")
            return None

    def retrieve_result(self):
        """
        This function concatenates the processed data for clustering.

        Returns:
            pd.DataFrame: The concatenated processed data for clustering.
        """
        return pd.concat([self.preprocess_data_for_clustering()])

    @staticmethod
    def refine_resulting_data(data: pd.DataFrame) -> pd.DataFrame:
        """
        This function removes columns from the dataframe
        that contain irradiance or temperature data.

        Args:
            data (pd.DataFrame): The dataframe to be refined.

        Returns:
            pd.DataFrame: The refined dataframe.
        """
        resulting_data = data.drop(
            [col for col in data.columns if "direct_normal_irradiance"
             in col or "temperature_2m" in col],
            axis=1).reset_index()
        return resulting_data

    def preprocess_data(self):
        """
        This function prepares the data for clustering.
        It extracts the relevant columns from the BOUM and weather data,
        corrects the data, samples the daily means, and creates pivot tables.
        It then appends the pivot tables to a final dataframe and returns the resulting data.

        Returns:
            pd.DataFrame: The processed data, or an empty DataFrame if an error occurred.

        Raises:
            ValueError: If an error occurred during data preprocessing.
        """
        try:
            self.boum_data = self.preprocess_timestamps()
            if self.boum_data is None:
                raise ValueError("Failed to preprocess timestamps in boum data.")

            self.boum_data = self.correct_data()
            if self.boum_data is None:
                raise ValueError("Failed to correct boum data.")

            self.boum_data, self.weather_data = self.rename_columns()

            aggregated_data = self.retrieve_result()
            if aggregated_data.empty:
                raise ValueError("Failed to preprocess data for clustering.")

            self.processed_data = self.refine_resulting_data(aggregated_data)
            if self.processed_data.empty:
                raise ValueError("Failed to process the data.")

            return self.processed_data

        except ValueError as value_error:
            print(f"ValueError occurred in data preprocessor: {value_error}")
            return None
        except Exception as exception:
            print(f"Exception occurred in data preprocessor: {exception}")
            return None