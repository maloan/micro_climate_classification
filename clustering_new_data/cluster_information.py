"""
A class for storing and retrieving information about temperature and radiation clusters.
"""


class ClusterInformation:
    """
    This class provides information about the extracted temperature and radiation clusters.

    Attributes:
        temperature_cluster (str): The temperature cluster,
        which can be one of 'cool', 'warm', 'hot', or 'unknown'.
        radiation_cluster (str): The radiation cluster,
        which can be one of 'dark', 'medium dark', 'medium bright', 'bright', or 'unknown'.
    """

    def __init__(self, temperature_cluster: str, radiation_cluster: str) -> None:
        """
        Initialize a new instance of the ClusterInformation class.

        Args:
            temperature_cluster (str): The temperature cluster.
            radiation_cluster (str): The radiation cluster.
        """
        self.temperature_cluster = temperature_cluster
        self.radiation_cluster = radiation_cluster

    def get_cluster_information(self) -> str:
        """
        This function returns a string containing information
        about the temperature and radiation clusters.

        Returns:
            str: A string containing information about the temperature and radiation clusters.
        """
        temp_info = self.get_temperature_cluster_information()
        rad_info = self.get_radiation_cluster_information()
        information = f"Temperature Cluster: {temp_info}\n\nRadiation Cluster: {rad_info}"
        return information

    def get_temperature_cluster_information(self):
        """
        This function returns a string containing information about the temperature cluster.

        Returns:
            str: A string containing information about the temperature cluster.
        """
        if self.temperature_cluster == 'cool':
            temp_info = """Cool Cluster
            - Average Temp: 18.6°C
            - Range: 7°C to 32°C
            - Peak Time: 1-2 PM"""
        elif self.temperature_cluster == 'warm':
            temp_info = """Warm Cluster
            - Average Temp: 20.2°C
            - Range: 8°C to 45°C
            - Peak Time: 2-3 PM"""
        elif self.temperature_cluster == 'hot':
            temp_info = """Hot Cluster
            - Average Temp: 19.1°C
            - Range: 5°C to 44°C
            - Peak Time: 1-2 PM"""
        else:
            temp_info = "Temperature Cluster: Information Unknown"
        return temp_info

    def get_radiation_cluster_information(self):
        """
        This function returns a string containing information about the radiation cluster.

        Returns:
            str: A string containing information about the radiation cluster.
        """
        if self.radiation_cluster == 'dark':
            rad_info = """Dark Cluster
            - Average Voltage: 2.8V
            - Peak Time: 8-9 AM"""
        elif self.radiation_cluster == 'medium dark':
            rad_info = """Medium Dark Cluster
            - Average Voltage: 2.9V
            - Peak Time: 10-11 AM"""
        elif self.radiation_cluster == 'medium bright':
            rad_info = """Medium Bright Cluster
            - Average Voltage: 3.4V
            - Peak Time: 11 AM-Noon"""
        elif self.radiation_cluster == 'bright':
            rad_info = """Bright Cluster
            - Average Voltage: 3.4V
            - Peak Time: 11 AM-Noon"""
        else:
            rad_info = "Radiation Cluster: Information Unknown"
        return rad_info
