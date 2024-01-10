"""
This module contains a function that calls the OpenWeatherMap API
to retrieve historical weather data.
"""
import pandas as pd
import requests


def call_historical_weather_data(lat: float, lon: float, start_date: str,
                                 end_date: str, hourly: bool,
                                 timezone: str) -> pd.DataFrame:
    """
    This function retrieves historical weather data from the OpenWeatherMap API.

    Parameters:
        lat (float): latitude of the location
        lon (float): longitude of the location
        start_date (str): start date of the data in YYYY-MM-DD format
        end_date (str): end date of the data in YYYY-MM-DD format
        hourly (bool): whether to retrieve hourly data or daily data
        timezone (str): timezone of the location

    Returns:
        pd.DataFrame: historical weather data
    """
    api_url = "https://archive-api.open-meteo.com/v1/archive"
    params = {"latitude": lat, "longitude": lon, "start_date": start_date,
              "end_date": end_date, "hourly": hourly,
              "timezone": timezone}
    response = requests.get(api_url, params=params, timeout=60)
    data = response.json()
    hist_weather = pd.DataFrame(data)
    hist_weather = hist_weather[hist_weather["is_day"] == 1]
    hist_weather = hist_weather.set_index("time")
    hist_weather.index = pd.to_datetime(hist_weather.index)
    hist_weather["month"] = hist_weather.index.month
    hist_weather = hist_weather.dropna()
    hist_weather.to_pickle("../data/hist_weather_pickled",
                           compression="infer", protocol=5)
    return hist_weather
