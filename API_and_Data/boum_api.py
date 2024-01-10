"""
API_and_Data/boum_api.py

This script is used to retrieve data from the Boum API for
a list of systems and save it as a CSV file.

The script requires the following files:
    - device_list.txt: file containing the list of devices to retrieve data for
    - boum_credentials_prod.txt: file containing the prod credentials for the Boum API
    - boum_credentials_dev.txt: file containing the dev credentials for the Boum API

The script creates the following files:
    -../data/boum_dataframe.measurements_YYYY-MM-DD.csv:
    a CSV file containing the data for each device
"""
import time
from asyncio.log import logger
from datetime import timedelta, datetime

import pandas as pd
from boum.api_client.constants import API_URL_PROD, API_URL_DEV
from boum.api_client.v1.client import ApiClient
from boum.resources.device import Device
from tqdm import tqdm

from API_and_Data.save_data import save_data

with open("../data/boum_credentials_prod.txt",
          encoding="utf-8", mode="r") as prod_credentials:
    username_prod = prod_credentials.readline().strip()
    password_prod = prod_credentials.readline().strip()
with open("../data/boum_credentials_dev.txt",
          encoding="utf-8", mode="r") as dev_credentials:
    username_dev = dev_credentials.readline().strip()
    password_dev = dev_credentials.readline().strip()


def open_device_list(device_list_file):
    """
    This function opens the device list file and reads the device IDs.

    Args:
        device_list_file (str): The path to the file containing the list of Boum device IDs

    Returns:
        list: A list of Boum device IDs
    """
    with open(f"../data/{device_list_file}", encoding="utf-8", mode="r") as f_device_list:
        device_list = f_device_list.read().splitlines()
    return device_list


def authenticate(mode):
    """
    This function authenticates with the Boum API using the provided credentials.

    Args:
        mode (str): The mode (production or development)

    Returns:
        ApiClient: The authenticated API client
    """
    if mode == "dev":
        client = ApiClient(username_dev, password_dev, base_url=API_URL_DEV)
    else:
        client = ApiClient(username_prod, password_prod, base_url=API_URL_PROD)
    client.connect()
    return client


def get_device_data(device_id: str, mode: str,
                    time_offset: datetime = datetime(2023, 10, 30),
                    days: int = 610, minutes: int = 60):
    """
    This function retrieves data from a Boum device.

    Args:
        device_id (str): The Boum device ID
        mode (str): The mode (production or development)
        time_offset (datetime): The start time for the data retrieval
        days (int): The number of days of data to retrieve
        minutes (int): The interval between data points (in minutes)

    Returns:
        pd.DataFrame: The data retrieved from the Boum device
    """
    client = authenticate(mode)
    device = Device(device_id, client)
    attempts = 0
    while attempts <= 35:
        try:
            return device.get_telemetry_data(start=time_offset - timedelta(days=days),
                                             end=time_offset,
                                             interval=timedelta(minutes=minutes))
        except ConnectionError as connection_error:
            logger.error("Connection error for device %s: %s",
                         device_id, connection_error)
        except TimeoutError as timeout_error:
            logger.error("Timeout error for device %s: %s",
                         device_id, timeout_error)
        attempts += 1
        time.sleep(2)  # Wait for 2 seconds before retrying
    return pd.DataFrame()


def create_boum_dataframe(sensor_names, boum_data):
    """
    This function creates a single dataframe from the data retrieved from all devices.

    Args:
        sensor_names (list): A list of sensor names
        boum_data (dict): A dictionary of dataframes,
        where the keys are the sensor names and the values are the data

    Returns:
        pd.DataFrame: A dataframe containing the data from all sensors
    """
    dfs = [boum_data[device_id] for device_id in sensor_names]
    dataframe = dfs[0]
    for column in range(len(dfs) - 1):
        column += 1
        dataframe = pd.merge_ordered(dataframe, dfs[column], on="timestamp")
    dataframe = dataframe.copy()
    dataframe["timestamp"] = pd.to_datetime(dataframe.timestamp).dt.tz_localize(None)
    return dataframe


def get_boum_data(device_list_file=None):
    """
    This function retrieves data from all Boum devices and creates a dataframe.

    Args:
        device_list_file (str): The path to the file containing
        the list of Boum device IDs (optional)

    Returns:
        pd.DataFrame: A dataframe containing the data from all sensors
    """
    if device_list_file is None:
        device_list_file = "../data/boum_device_list.txt"
    device_list = open_device_list(device_list_file)
    boum_data = {}
    for device_id in tqdm(device_list, desc="Processing devices"):
        time.sleep(5)
        try:
            data = get_device_data(device_id, "prod")
            if pd.DataFrame(data).empty:
                data = get_device_data(device_id, mode="dev")
            if not pd.DataFrame(data).empty:
                dataframe = pd.DataFrame(data)
                boum_data[device_id] = dataframe
        except Exception as exception:
            print(f"Error processing device {device_id}: {exception}")
    if not boum_data:
        return pd.DataFrame()
    sensor_names = list(boum_data)
    return create_boum_dataframe(sensor_names, boum_data)


if __name__ == "__main__":
    boum_dataframe = get_boum_data()
    save_data(name="boum-dataframe", data=boum_dataframe)
    print(boum_dataframe)

# %%
