"""
This script is used to retrieve data from the Fyta API and save it as a CSV file.

The script requires the following files:
    - fyta_credentials.txt: A file containing the Fyta username and password

The script creates the following files:
    -../data/fyta_dataframe.measurements_YYYY-MM-DD.csv:
    a CSV file containing the combined dataframe for each sensor for each plant.
"""
from datetime import datetime

import pandas as pd
import requests

# Base URL for Fyta API
BASE_URL = "https://web.fyta.de/api"

# Read Fyta credentials from file
with open("../data/fyta_credentials.txt", encoding="utf-8", mode="r") as fyta_file:
    username = fyta_file.readline().strip()
    password = fyta_file.readline().strip()

# Dictionary mapping sensor location to sensor IDs
sensor_locations = {"tank": [21328, 21335, 14541, 21355, 21352, 21349, 21344, 21339],
                    "sun": [21329, 21332, 21356, 21347, 21337, 21353, 21350, 21326, 21345, 21341],
                    "pot": [21331, 21334, 14539, 21348, 21338, 21354, 21351, 21327, 21346, 21343]}


def authentication(user, pwd):
    """
    Authenticates with the Fyta API using the provided username and password.

    Args:
        user (str): Fyta username
        pwd (str): Fyta password

    Returns:
        dict: Dictionary containing the authentication token and expiration time
    """
    headers = {"Content-Type": "application/json"}
    login = {"email": user, "password": pwd}
    auth = requests.post(f"{BASE_URL}/auth/login", headers=headers, json=login, timeout=60).json()
    headers = {"Authorization": f"Bearer {auth['access_token']}",
               "Content-Type": "application/json"}
    return headers


def get_plants(headers):
    """
    Retrieves the list of plant associated with the authenticated user.

    Args:
        headers (dict): Dictionary containing the authentication token

    Returns:
        dict: Dictionary containing the plant list and pagination information
    """
    return requests.get(f"{BASE_URL}/user-plant", headers=headers, timeout=60).json()


def get_sensor_ids(plants):
    """
    Retrieves a list of sensor IDs from the list of plants.

    Args:
        plants (dict): Dictionary containing the plant list

    Returns:
        list: List of sensor IDs
    """
    return [plant["id"] for plant in plants["plants"]]


def get_fyta_data(user=username, pwd=password):
    """
    Retrieves data from Fyta and saves it as a CSV file.

    Args:
        user (str): Fyta username (default: username from credential file)
        pwd (str): Fyta password (default: password from credential file)

    Returns:
        pandas.DataFrame: Combined data from Fyta sensors
    """
    headers = authentication(user, pwd)
    plants = get_plants(headers)
    sensor_ids = get_sensor_ids(plants)
    measurements = {}
    for sensor_id in sensor_ids:
        data = {"search": {"timeline": "month"}}
        timeseries = requests.post(
            f"{BASE_URL}/user-plant/measurements/{sensor_id}",
            headers=headers, json=data, timeout=60).json()
        key_name = f"{sensor_id}"
        measurements[key_name] = pd.DataFrame.from_dict(timeseries["measurements"])

    for sensor, value in measurements.items():
        for col in value.columns:
            measurements[sensor].rename(
                columns={col: col.replace(col, f"{col}_{sensor[-5:]}")}, inplace=True)
            measurements[sensor].rename(
                columns={measurements[sensor].columns[-1]: "timestamp"}, inplace=True)
    sensor_names = list(measurements)
    return create_dataframe(sensor_names, measurements, sensor_locations)


def create_dataframe(sensor_names, measurements, sensor_location):
    """
    Combines the data from each sensor into a single dataframe.

    Args:
        sensor_names (list): List of sensor names
        measurements (dict): Dictionary of sensor dataframes
        sensor_location (dict): Dictionary mapping sensor location to sensor IDs

    Returns:
        pandas.DataFrame: Combined data from Fyta sensors
    """
    dfs = [measurements[sensor] for sensor in sensor_names]
    dataframe = dfs[0]
    for cols in range(1, len(dfs)):
        if "timestamp" in dfs[cols]:
            dataframe = pd.merge_ordered(dataframe, dfs[cols], on="timestamp")
    dataframe = dataframe.copy()
    for location in sensor_location:
        for sensor in sensor_location[location]:
            name = f"location_{sensor}"
            dataframe[name] = location
    if "timestamp" in dataframe:
        dataframe["timestamp"] = pd.to_datetime(dataframe["timestamp"])
    dataframe = pd.DataFrame(dataframe)
    current_date = datetime.now().date()
    filename = f"data/fyta-dataframe.measurements_{current_date}.csv"
    dataframe.to_csv(filename, index=False)
    print(f"Data saved successfully as {filename}.")
    return dataframe


if __name__ == "__main__":
    fyta_df = get_fyta_data(username, password)
    print(fyta_df)
