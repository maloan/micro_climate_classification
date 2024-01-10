"""
This script is responsible for loading and manipulating the survey data.
"""
import logging
import os

import pandas as pd


class SurveyData:
    """
    The SurveyData class is responsible for loading and manipulating the survey data.

    Attributes:
        path (str): The path to the CSV file containing the survey data.
        survey_data (pd.DataFrame): The DataFrame containing the survey data.

    Methods:
        get_survey_data: Returns the DataFrame containing the survey data.
        extract_coordination_dict: Returns a dictionary
        mapping device IDs to (latitude, longitude) coordinates.
    """

    def __init__(self):
        """
        Initializes the SurveyData class.
        """
        self.path = "../data/survey_data.csv"
        self.survey_data = self.get_survey_data()

    def get_survey_data(self):
        """
        Returns the DataFrame containing the survey data.

        Returns:
            pd.DataFrame: The DataFrame containing the survey data.

        Raises:
            FileNotFoundError: If the CSV file containing the survey data does not exist.
            pd.errors.EmptyDataError: If the CSV file containing the survey data is empty.
        """
        if not os.path.exists(self.path):
            logging.error("Error: CSV file does not exist.")
            return None
        try:
            return pd.read_csv(self.path)
        except pd.errors.EmptyDataError:
            logging.error("Error: CSV file is empty.")
            return None

    def extract_coordination_dict(self):
        """
        Returns a dictionary mapping device IDs to (latitude, longitude) coordinates.

        Returns:
            dict: A dictionary mapping device IDs to (latitude, longitude) coordinates.

        Raises:
            ValueError: If the survey data is not loaded.
        """
        if self.survey_data is None:
            return None
        return {self.survey_data["deviceId_boum"].iloc[i]: (
            self.survey_data["latitude"].iloc[i],
            self.survey_data["longitude"].iloc[i]) for i in
            range(len(self.survey_data))}
