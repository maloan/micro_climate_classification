"""
This script is used to retrieve data from various sources and save it as a CSV file.
"""
import os

import pandas as pd

from API_and_Data.merge_data import merge_dataframe
from API_and_Data.boum_api import get_boum_data
from API_and_Data.fyta_api import get_fyta_data
from API_and_Data.weather_api import get_weather_data


class GetData:
    """
    The GetData class is responsible for retrieving and merging data from various sources.
    """

    def __init__(self):
        """
        Initializes the GetData class.
        """
        self.path = "../data/"

    @staticmethod
    def get_data(coordinates_dict=None, norm=False):
        """
        Retrieves data from various sources and returns it as a Pandas DataFrame.

        Args:
            coordinates_dict (dict):
            a dictionary containing the coordinates of the location for
            which data is to be retrieved
            norm (bool): a boolean indicating whether to normalize the data or not

        Returns:
            pandas.DataFrame: the retrieved data
        """
        print("Retrieving weather_data...")
        boum_dataframe = get_boum_data()
        fyta_dataframe = get_fyta_data()
        weather_dataframe = get_weather_data(coordinates_dict)
        return merge_dataframe(boum_dataframe, fyta_dataframe, weather_dataframe, norm=norm)

    def merge_all_dataframes(self):
        """
        Merges all dataframes into one dataframe.

        Returns:
            pandas.DataFrame: the merged data
        """
        boum_cdf = pd.DataFrame()
        fyta_cdf = pd.DataFrame()
        weather_cdf = pd.DataFrame()
        for file in os.listdir(self.path):
            if file.startswith("boum-dataframe.measurement"):
                boum_cdf1 = pd.read_csv("../weather_data/" + file, low_memory=False)
                boum_cdf = pd.concat([boum_cdf, boum_cdf1])
            elif file.startswith("fyta-dataframe.measurement"):
                fyta_cdf1 = pd.read_csv("../weather_data/" + file, low_memory=False)
                fyta_cdf = pd.concat([fyta_cdf, fyta_cdf1])
            elif file.startswith("weather-dataframe.measurement"):
                weather_cdf1 = pd.read_csv("../weather_data/" + file, low_memory=False)
                weather_cdf = pd.concat([weather_cdf, weather_cdf1])
        return merge_dataframe(boum_cdf, fyta_cdf, weather_cdf, norm=False)


if __name__ == "__main__":
    data = GetData()
    df = data.get_data()
    print(df)
