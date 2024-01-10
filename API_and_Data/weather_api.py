"""
This module contains a function that retrieves weather data from the Open Meteo API.
"""
from datetime import date

import pandas as pd
import requests

from API_and_Data.save_data import save_data


def get_weather_data(coordinates_dict: dict, timezone: str = "Europe/Berlin"):
    """
    This function retrieves weather data from the Open Meteo API for a given set of coordinates.

    Args:
        coordinates_dict (dict): A dictionary containing
        the coordinates as (latitude, longitude) pairs.
        timezone (str, optional): The timezone for
        the requested data (default: "Europe/Berlin").

    Returns:
        pd.DataFrame: A pandas dataframe containing the weather data.
    """
    weather_data = []
    forecast_base_url = "https://archive-api.open-meteo.com/v1"
    headers = {"Content-Type": "application/json"}
    hourly_forecast_data = ["temperature_2m", "direct_normal_irradiance"]
    for key, (latitude, longitude) in coordinates_dict.items():
        url = (f"{forecast_base_url}/archive?latitude={latitude}"
               f"&longitude={longitude}&start_date=2018-01-01&"
               f"end_date={date.today()}"
               f"&hourly={','.join(hourly_forecast_data)}"
               f"&timezone={timezone}")
        response = requests.get(url, headers=headers, timeout=60)
        weather_data.append(response.json())
    return create_dataframe(weather_data, list(coordinates_dict.keys()))


def create_dataframe(weather_data: list, keys: list):
    """
    This function creates a pandas dataframe from the retrieved weather data.

    Args:
        weather_data (list): A list of dictionaries containing the weather data.
        keys (list): A list of the keys from the coordinates_dict.

    Returns:
        pd.DataFrame: A pandas dataframe containing the weather data.
    """
    dfs = [pd.DataFrame(data) for data in weather_data]
    dataframe = pd.concat(dfs, axis=1)
    dataframe.columns = [f"{col}_{key[:8]}" for i, key in enumerate(keys) for col in dfs[i].columns]
    dataframe.rename(columns={dataframe.columns[0]: "timestamp"}, inplace=True)
    dataframe["timestamp"] = pd.to_datetime(dataframe["timestamp"])
    save_data("weather-dataframe", dataframe)
    return dataframe
