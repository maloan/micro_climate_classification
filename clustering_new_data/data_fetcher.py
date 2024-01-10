"""
This module contains the functions to retrieve data from the Boum API and the OpenWeatherMap API.
"""

import logging
import time
from asyncio.log import logger
from datetime import datetime, timedelta

import pandas as pd
import requests
from boum.api_client.constants import API_URL_PROD, API_URL_DEV
from boum.api_client.v1.client import ApiClient
from boum.resources.device import Device
from geopy import Nominatim
from geopy.extra.rate_limiter import RateLimiter

logging.basicConfig(level=logging.INFO)


class DataFetcher:
    """
    The DataFetcher class is responsible for retrieving data
    from the Boum API and the OpenWeatherMap API.

    Args:
        user_data (dict): A dictionary containing the user-input data, including
            the target month, year, city, postal code, address, street number, and device ID.

    Attributes:
        boum_data (dict): A dictionary containing the BOUM data for each device.
        weather_data (list): A list containing the weather data for the target month.
        user_data (dict): The user-input data.
        coordinates (dict): The coordinates for the target location.
        logger (logging.Logger): The logger for the class.
    """

    def __init__(self, user_data):
        self.boum_data = {}
        self.weather_data = []
        self.target_date = None
        self.user_data = user_data
        self.coordinates = None
        self.logger = logging.getLogger(__name__)
        self.fetch_data()

    @staticmethod
    def get_credentials():
        """
        This function retrieves the Boum API credentials from the specified files.

        Returns:
            A tuple containing the Boum API credentials for
            the production and development environments.
        """
        with open("../data/boum_credentials_prod.txt",
                  encoding="utf-8", mode="r") as prod_credentials:
            username_prod = prod_credentials.readline().strip()
            password_prod = prod_credentials.readline().strip()
        with open("../data/boum_credentials_dev.txt",
                  encoding="utf-8", mode="r") as dev_credentials:
            username_dev = dev_credentials.readline().strip()
            password_dev = dev_credentials.readline().strip()
        return username_prod, password_prod, username_dev, password_dev

    def process_date_input(self):
        """
        This function processes the user input for the target month and year.

        Parameters:
            self (DataFetcher): The DataFetcher object.

        Returns:
            The target date as a datetime object.
        """
        self.target_date = datetime.strptime(
            f'{self.user_data.get("year")}-{self.user_data.get("month")}',
            '%Y-%m')
        return self.target_date

    def get_location(self):
        """
        This function attempts to retrieve the coordinates for
        the target location using the Nominatim API.

        Parameters:
            self (DataFetcher): The DataFetcher object.

        Returns:
            A dictionary containing the latitude and longitude for the target location,
            or None if the location could not be found.

        Raises:
            Exception: If an error occurs while attempting to retrieve the location.
        """

        locator = Nominatim(user_agent="cluster_micro_climate")
        geocode = RateLimiter(locator.geocode)
        full_address = (f"{self.user_data.get('street_name')}, "
                        f"{self.user_data.get('street_number')}, "
                        f"{self.user_data.get('postal_code')}, "
                        f"{self.user_data.get('city')}, 'Switzerland'")
        location = geocode(full_address)
        if location:
            return {"latitude": location.latitude, "longitude": location.longitude}
        print("Unable to find location. Please check the address details.")
        return None

    def authenticate(self, mode):
        """
        Authenticates the API client with the specified credentials and environment.

        Args:
            mode (str): The environment to authenticate against either "dev" or "prod".

        Returns:
            The authenticated API client.

        Raises:
            ValueError: If an invalid environment is specified.
        """
        (username_prod, password_prod,
         username_dev, password_dev) = self.get_credentials()
        if mode == "dev":
            client = ApiClient(username_dev, password_dev, base_url=API_URL_DEV)
        elif mode == "prod":
            client = ApiClient(username_prod, password_prod, base_url=API_URL_PROD)
        else:
            raise ValueError(f"Invalid environment: {mode}. Must be 'dev' or 'prod'.")
        client.connect()
        return client

    def get_device_data(self, mode, days=30):
        """
        This function retrieves the data for a specific device from the Boum API.

        Args:
            mode (str): The environment to authenticate against either "dev" or "prod".
            days (int, optional): The number of days of data to retrieve (default is 30).

        Returns:
            A pandas dataframe containing the data for the specified device.

        Raises:
            ValueError: If an invalid environment is specified.
            Exception: If an error occurs while retrieving the data.
        """
        client = self.authenticate(mode)
        device = Device(self.user_data.get('device_id'), client)
        attempts = 0
        max_attempts = 30

        while attempts < max_attempts:
            try:
                return device.get_telemetry_data(start=self.target_date - timedelta(days=days),
                                                 end=self.target_date + timedelta(days=days),
                                                 interval=timedelta(minutes=60))
            except ConnectionError as connection_error:
                logger.error("Connection error for device %s: %s",
                             self.user_data.get('device_id'), connection_error)
            except TimeoutError as timeout_error:
                logger.error("Timeout error for device %s: %s",
                             self.user_data.get('device_id'), timeout_error)
            attempts += 1
            time.sleep(2)  # Wait for 2 seconds before retrying

        logger.error("Failed to retrieve data after %s attempts", max_attempts)
        return pd.DataFrame()

    def create_boum_dataframe(self, sensor_names):
        """
        This function merges the dataframes for each sensor into a single dataframe.

        Args:
            sensor_names (list): A list of the sensor names.

        Returns:
            A pandas dataframe containing the merged data.
        """
        dfs = [self.boum_data[device_id] for device_id in sensor_names]
        dataframe = dfs[0]
        for device in range(len(dfs) - 1):
            device += 1
            dataframe = pd.merge_ordered(dataframe, dfs[device], on="timestamp")
        dataframe = dataframe.copy()
        dataframe["timestamp"] = pd.to_datetime(dataframe.timestamp).dt.tz_localize(None)
        return dataframe

    def get_boum_data(self):
        """
        This function retrieves the boum data for the device.
        Args:
            self (DataFetcher): The DataFetcher object.

        Returns:
            pd.DataFrame: A pandas dataframe containing the boum data for the device.
        """
        device_id = self.user_data.get("device_id")[:8]
        try:
            data = self.get_device_data("prod")
            if pd.DataFrame(data).empty:
                data = self.get_device_data("dev")
            if not pd.DataFrame(data).empty:
                dataframe = pd.DataFrame(data)
                dataframe.rename(columns=lambda col: f"{col}", inplace=True)
                dataframe.rename(columns={dataframe.columns[-1]: "timestamp"}, inplace=True)
                self.boum_data[device_id] = dataframe
                print(f"Data for device {device_id} retrieved")
            else:
                print(f"No data for device {device_id}")
        except ConnectionError as connection_error:
            logger.error("Connection error for device %s: %s",
                         self.user_data.get('device_id'), connection_error)
        except pd.errors.EmptyDataError as empty_data_error:
            print(f"Empty data error for device {device_id}: {empty_data_error}")

        if not self.boum_data:
            return pd.DataFrame()

        for device_id, value in self.boum_data.items():
            for col in value.columns:
                self.boum_data[device_id].rename(
                    columns={col: col.replace(
                        col, f"{col}_boum_{device_id[:8]}")},
                    inplace=True)
                self.boum_data[device_id].rename(
                    columns={self.boum_data[device_id].columns[-1]: "timestamp"},
                    inplace=True)

        sensor_names = list(self.boum_data)
        return self.create_boum_dataframe(sensor_names)

    def get_weather_data(self):
        """
        This function retrieves the weather data for the target month and location.

        Parameters:
            self (DataFetcher): The DataFetcher object.

        Returns:
            A pandas dataframe containing the weather data.
        """
        forecast_base_url = "http://archive-api.open-meteo.com/v1"
        headers = {"Content-Type": "application/json"}
        hourly_forecast_data = ["temperature_2m", "direct_normal_irradiance", ]
        start_date = (self.target_date - timedelta(30)).strftime('%Y-%m-%d')
        end_date = (self.target_date + timedelta(30)).strftime('%Y-%m-%d')

        url = (f"{forecast_base_url}/archive?latitude={self.coordinates['latitude']}&"
               f"longitude={self.coordinates['longitude']}&"
               f"start_date={start_date}&"
               f"end_date={end_date}&"
               f"hourly={','.join(hourly_forecast_data)}"
               f"&timezone=Europe/Berlin")
        response = requests.get(url, headers=headers, timeout=60)
        self.weather_data = response.json()['hourly']
        return self.create_weather_dataframe(self.user_data.get('device_id'))

    def create_weather_dataframe(self, key):
        """
        This function creates a pandas dataframe from the weather data.

        Args:
            key (str): The unique key for the device.

        Returns:
            A pandas dataframe containing the weather data.
        """
        dataframe = pd.DataFrame(self.weather_data)
        dataframe.columns = [f"{col}_{key[:8]}" for col in dataframe.columns]
        dataframe.rename(columns={f"time_{key[:8]}": "timestamp"}, inplace=True)
        dataframe["timestamp"] = pd.to_datetime(dataframe["timestamp"])
        return dataframe

    def fetch_data(self):
        """
        This function retrieves the data for the specified month and location.

        Parameters:
            self (DataFetcher): The DataFetcher object.

        Returns:
            A tuple containing the device ID, coordinates,
            target month, BOUM data, and weather data.
        """
        try:
            self.target_date = self.process_date_input()
            self.coordinates = self.get_location()
            self.boum_data = self.get_boum_data()
            self.weather_data = self.get_weather_data()
            return (self.user_data.get('device_id'), self.coordinates,
                    self.user_data.get('target_month'), self.boum_data, self.weather_data)
        except Exception as exception:
            logger.error("Error fetching data: %s", exception)
            return None

# %%
