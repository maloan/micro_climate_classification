"""
This class contains the functions to preprocess and predict the cluster labels for the given data.
"""
import joblib
import pandas as pd


class ClusterPredictor:
    """
    This class contains the functions to preprocess and
    predict the cluster labels for the given data.

    Attributes:
        data (pd.DataFrame): The input data to be used for prediction.
        mode (str): The mode of prediction, either 'temperature' or 'radiation'.
    """

    def __init__(self, data, mode):
        """
        Initializes the class attributes.

        Args:
            data (pd.DataFrame): The input data to be used for prediction.
            mode (str): The mode of prediction, either 'temperature' or 'radiation'.
        """
        self.data = data
        self.mode = mode
        try:
            self.temperature_model = [joblib.load("../model/scaler_temperature.pkl"),
                                      joblib.load("../model/temperature_clusters.pkl"),
                                      joblib.load("../model/pca_temperature.pkl")]

            self.radiation_model = [joblib.load("../model/scaler_radiation.pkl"),
                                    joblib.load("../model/radiation_clusters.pkl"),
                                    joblib.load("../model/pca_radiation.pkl")]

        except FileNotFoundError as file_not_found_error:
            raise FileNotFoundError(f'Model file not found: {file_not_found_error}') \
                from file_not_found_error

    def preprocess_data(self):
        """
        Preprocesses the input data by applying the appropriate scaling
        and dimensionality reduction techniques.

        Returns:
            np.ndarray: The preprocessed data.
        """
        if self.mode == 'temperature':
            df_scaled = self.temperature_model[0].transform(
                self.data.reindex(range(4), axis=1).interpolate(axis=1).bfill(axis=1))
            df_pca = self.temperature_model[2].transform(df_scaled)
        else:
            df_scaled = self.radiation_model[0].transform(
                self.data.reindex(range(4), axis=1).interpolate(axis=1).bfill(axis=1))
            df_pca = self.radiation_model[2].transform(df_scaled)
        return df_pca

    def label_cluster(self, cluster_number):
        """
        Maps the cluster numbers to labels.

        Args:
            cluster_number (int): The cluster number to be mapped to a label.

        Returns:
            str: The mapped label for the given cluster number.

        Raises:
            ValueError: If the cluster number is not found in the mapping.
        """
        if self.mode == 'radiation':
            cluster_mapping = {3: 'dark', 1: 'medium dark', 0: 'medium bright', 2: 'bright'}
        else:
            cluster_mapping = {0: 'cool', 2: 'warm', 1: 'hot'}
        return cluster_mapping.get(cluster_number, "Unknown")

    def predict_cluster(self):
        """
        Predicts the clusters for the input data.

        Raises:
            ValueError: If the input data is not a pandas DataFrame.
            ValueError: If the mode is not 'radiation' or 'temperature'.

        Returns:
            str: The predicted cluster label.
        """
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError("Input must be a pandas DataFrame")

        if self.mode not in ["radiation", "temperature"]:
            raise ValueError("Mode must be either 'radiation' or 'temperature'")

        try:
            df_preprocessed = self.preprocess_data()

            if self.mode == "radiation":
                cluster_number = self.radiation_model[1].predict(df_preprocessed)[0]
            else:
                cluster_number = self.temperature_model[1].predict(df_preprocessed)[0]
            cluster_label = self.label_cluster(int(cluster_number))
            return cluster_label
        except ValueError as value_error:
            raise value_error from value_error
