"""
This file contains the main function for the clustering application.

Author: Ananda Kurth
Email: ananda.kurth@unifr.ch
"""
import tkinter as tk
from tkinter import messagebox

import pandas as pd

from clustering_new_data import user_interface
from clustering_new_data.cluster_information import ClusterInformation
from clustering_new_data.cluster_predictor import ClusterPredictor
from clustering_new_data.data_fetcher import DataFetcher
from clustering_new_data.data_preprocessor import DataPreprocessor
from clustering_new_data.data_processor import DataProcessor


def main():
    """
    This function initializes the Tkinter GUI, collects user input, and
    invokes the process_and_predict_data function to process and predict
    the clusters if valid user input is provided.

    Raises:
        Exception: If an unexpected error occurs.
    """
    try:
        root = tk.Tk()
        root.withdraw()
        user_data = user_interface.get_user_input()
        if user_data:
            process_and_predict_data(user_data)
        root.destroy()
    except Exception as exception:
        messagebox.showerror("Error", f"An unexpected error occurred: {exception}")


def process_and_predict_data(user_data: dict) -> None:
    """
    This function processes the user input data and invokes
    the predict_clusters function to predict the clusters.

    Args:
        user_data (dict): The user input data.

    Raises:
        ValueError: If the user data is invalid.
        IOError: If there is an error reading the input files.
    """
    try:
        data_fetcher = DataFetcher(user_data)
        boum_data = data_fetcher.boum_data
        weather_data = data_fetcher.weather_data
        target_date = data_fetcher.target_date.month
        device_id = data_fetcher.user_data.get('device_id')[:8]
        data_preprocessor = DataPreprocessor(boum_data, weather_data, target_date, device_id)
        processed_data = data_preprocessor.preprocess_data()
        temperature_cluster, radiation_cluster = predict_clusters(processed_data)
        cluster_information = ClusterInformation(temperature_cluster, radiation_cluster)
        information = cluster_information.get_cluster_information()
        print(information)
        print_message(information)
    except ValueError as value_error:
        messagebox.showerror("Validation Error", str(value_error))
    except IOError as io_error:
        messagebox.showerror("File Error", str(io_error))


def predict_clusters(processed_data):
    """
    This function takes in the processed data and
    predicts the clusters for the temperature and radiation data.

    Args:
        processed_data (DataFrame): The processed data containing the features and labels.

    Returns:
        tuple: A tuple containing the predicted clusters for the temperature and radiation data.

    Raises:
        ValueError: If the input data is not a pd DataFrame.
    """
    if not isinstance(processed_data, pd.DataFrame):
        raise ValueError("The input data must be a pandas DataFrame.")
    data_processor_temperature = DataProcessor(processed_data, 'temperature')
    result_data_temperature = data_processor_temperature.process_data()
    predictor_temperature = ClusterPredictor(result_data_temperature, "temperature")
    temperature_cluster = predictor_temperature.predict_cluster()
    data_processor_radiation = DataProcessor(processed_data, 'radiation')
    result_data_radiation = data_processor_radiation.process_data()
    predictor_radiation = ClusterPredictor(result_data_radiation, "radiation")
    radiation_cluster = predictor_radiation.predict_cluster()
    return temperature_cluster, radiation_cluster


def print_message(information):
    """
    This function prints the information to the user.

    Args:
        information (str): The information to be printed to the user.
    """
    messagebox.showinfo("Prediction Results", information)


if __name__ == "__main__":
    main()

# %%
