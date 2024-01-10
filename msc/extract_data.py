"""
This module contains a class for extracting data from the raw data.
"""
from datetime import timedelta

import numpy as np
import pandas as pd


class ExtractData:
    """
    This class contains methods for extracting data from the raw data.
    """

    def __init__(self, df, number_of_days):
        """
        Initialize the ExtractData class.

        Args:
            df (pd.DataFrame): The raw data.
            number_of_days (int): The number of days of data to use.
        """
        self.num_days = number_of_days
        self.data = df
        self.sensor_dict = {"loc_1": ["21328", "21329", "21331"], "loc_0": ["14541", "21356", "14539"],
                            "loc_2": ["21335", "21332", "21334"], "loc_4": ["21349", "21350", "21351"],
                            "loc_9": ["21341", "21343"], "loc_6": ["21355", "21347", "21348"],
                            "loc_5": ["21337", "21338"], "loc_8": ["21326", "21327"],
                            "loc_3": ["21344", "21345", "21346"], "loc_7": ["21352", "21353", "21354"]}
        self.device_dict = {"loc_1": "655c77c8-0b0f-47c7-9f6c-fe517756829e",
                            "loc_0": "13235f69-0f74-4ef7-955d-848e831ffc3c",
                            "loc_2": "a2146308-f5e9-4cfe-a8c5-7b84cb4f70af",
                            "loc_4": "2a650b37-9645-46e0-825e-4a5319c09b03",
                            "loc_9": "32a5c848-366d-4029-8861-9689acf35b85",
                            "loc_6": "188be60e-3894-4e80-8850-165ba1e0061c",
                            "loc_5": "a27e798c-e69c-4603-b720-d195be6c8623",
                            "loc_8": "64f7fddf-01ac-4826-aaab-fcf4232e5bc6",
                            "loc_3": "cc1b8cb9-cafb-4bcf-b346-f4009c0403c8",
                            "loc_7": "5fe95b01-dce7-4c29-aae6-a39009f9e166"}
        self.tank_sensor_list = ["21328", "21349", "21352", "21335", "14541", "21355", "21344", ]
        self.sun_sensor_list = ["21329", "21332", "21356", "21347", "21337", "21353", "21350", "21326", "21345",
                                "21341"]
        self.sun_tank_sensor_list = ["21328", "21335", "14541", "21355", "21352", "21349", "21344", "21329", "21332",
                                     "21356", "21347", "21337", "21353", "21350", "21326", "21345", "21341"]
        self.orientation_dict = {"N": "a2146308-f5e9-4cfe-a8c5-7b84cb4f70af, "
                                      "21335, 21332, 21334", "E": "5fe95b01-dce7-4c29-aae6-a39009f9e166, "
                                                                  "587e4fdc-7241-4eec-9603-46ef4c5a6a01,"
                                                                  "68979444-6c7a-4a3e-985d-c92cc5b1f713,"
                                                                  "0e511a95-101b-4b6c-bc7a-e613be938ff5, "
                                                                  "e35608d7-3d70-473d-86cd-bca176d31bdd, "
                                                                  "995e0d31-3a6c-479f-935c-d1bb7ee3e578, "
                                                                  "61c434e0-69c2-4358-a8dc-35ad45eefb4b, "
                                                                  "8bef9470-9719-4c35-b8a9-71cb96c7dc3b, "
                                                                  "613fd40a-0b0c-4134-a379-651d9c88cebb,"
                                                                  "21352, 21353, 21354",
                                 "S": "188be60e-3894-4e80-8850-165ba1e0061c, "
                                      "655c77c8-0b0f-47c7-9f6c-fe517756829e,"
                                      "13235f69-0f74-4ef7-955d-848e831ffc3c, cc1b8cb9-cafb-4bcf-b346-f4009c0403c8,"
                                      "32a5c848-366d-4029-8861-9689acf35b85, 54fcc077-dc16-4e9b-875c-1ee00b430094,"
                                      "84abf531-db6f-4906-8a94-eca491b65679,2ede5849-e317-4139-be09-bb1312984fa7,"
                                      "d0611412-4fde-4daa-9e27-af31e9c90075,b504b5bf-8581-442c-888d-a3fdf7e1cd0e,"
                                      "0c15a648-3980-435f-8054-fd7655e22fbd,6f655cfb-2fb5-4f1b-afde-0271a212a7ef,"
                                      "045259fa-02a1-40e4-8263-441acbbc4cd4,23bb2b14-d004-47ae-89cc-b8ca2c51f2cf,"
                                      "a4ab53f6-10cc-4574-8e48-bd3759f919d1,d4f22445-4d03-4bce-8411-84c9a04abe29,"
                                      "188be60e-3894-4e80-8850-165ba1e0061c, 21339, 21341, 21343, 14541, 21356, 14539,"
                                      "21355, 21347, 21348, 21344, 21345,21346, 21328, 21329,21331",
                                 "W": "89199585-4f2f-466c-8f5a-beb40b02c452,8eb17c70-dfec-44a0-b327-0ed890544b77,"
                                      "fd236b88-0eed-4a75-9c55-f2bc8852d909,658e3260-b994-49a0-9903-3e804df76d54,"
                                      "e9b34a79-a4a2-4f0f-b46b-a86ae6fcc5a0,f8959e3a-fac2-4e5b-bcf1-a8e413d2e070,"
                                      "28eef71d-270a-4820-8fbd-6f051416c64d,dde5ad50-f8b4-4006-9f75-b369137c1268,"
                                      "cd56fb49-b883-4fab-b45e-20802aab4a0e,c8a40a31-18b1-4c06-9b06-bdc5fd5bea10,"
                                      "2a650b37-9645-46e0-825e-4a5319c09b03,a27e798c-e69c-4603-b720-d195be6c8623,"
                                      "64f7fddf-01ac-4826-aaab-fcf4232e5bc6,21349, 21350, 21351, 21337, "
                                      "21338, 14540, 21326, 21327", }

        self.device_list = ["54fcc077-dc16-4e9b-875c-1ee00b430094", "84abf531-db6f-4906-8a94-eca491b65679",
                            "89199585-4f2f-466c-8f5a-beb40b02c452", "8eb17c70-dfec-44a0-b327-0ed890544b77",
                            "587e4fdc-7241-4eec-9603-46ef4c5a6a01", "68979444-6c7a-4a3e-985d-c92cc5b1f713",
                            "2ede5849-e317-4139-be09-bb1312984fa7", "fd236b88-0eed-4a75-9c55-f2bc8852d909",
                            "658e3260-b994-49a0-9903-3e804df76d54", "e9b34a79-a4a2-4f0f-b46b-a86ae6fcc5a0",
                            "d0611412-4fde-4daa-9e27-af31e9c90075", "f8959e3a-fac2-4e5b-bcf1-a8e413d2e070",
                            "b504b5bf-8581-442c-888d-a3fdf7e1cd0e", "28eef71d-270a-4820-8fbd-6f051416c64d",
                            "0e511a95-101b-4b6c-bc7a-e613be938ff5", "0c15a648-3980-435f-8054-fd7655e22fbd",
                            "dde5ad50-f8b4-4006-9f75-b369137c1268", "cd56fb49-b883-4fab-b45e-20802aab4a0e",
                            "e35608d7-3d70-473d-86cd-bca176d31bdd", "995e0d31-3a6c-479f-935c-d1bb7ee3e578",
                            "61c434e0-69c2-4358-a8dc-35ad45eefb4b", "6f655cfb-2fb5-4f1b-afde-0271a212a7ef",
                            "045259fa-02a1-40e4-8263-441acbbc4cd4", "c8a40a31-18b1-4c06-9b06-bdc5fd5bea10",
                            "8bef9470-9719-4c35-b8a9-71cb96c7dc3b", "613fd40a-0b0c-4134-a379-651d9c88cebb",
                            "23bb2b14-d004-47ae-89cc-b8ca2c51f2cf", "a4ab53f6-10cc-4574-8e48-bd3759f919d1",
                            "d4f22445-4d03-4bce-8411-84c9a04abe29", "32a5c848-366d-4029-8861-9689acf35b85",
                            "cc1b8cb9-cafb-4bcf-b346-f4009c0403c8", "a2146308-f5e9-4cfe-a8c5-7b84cb4f70af",
                            "655c77c8-0b0f-47c7-9f6c-fe517756829e", "2a650b37-9645-46e0-825e-4a5319c09b03",
                            "13235f69-0f74-4ef7-955d-848e831ffc3c", "a27e798c-e69c-4603-b720-d195be6c8623",
                            "64f7fddf-01ac-4826-aaab-fcf4232e5bc6", "188be60e-3894-4e80-8850-165ba1e0061c",
                            "5fe95b01-dce7-4c29-aae6-a39009f9e166", ]
        self.sensor_location = {"tank": [21328, 21335, 14541, 21355, 21352, 21349, 21344, 21339],
                                "sun": [21329, 21332, 21356, 21347, 21337, 21353, 21350, 21326, 21345, 21341, ],
                                "pot": [21331, 21334, 14539, 21348, 21338, 21354, 21351, 21327, 21346, 21343, ]}
        self.location = ["sun", "tank", "pot"]
        self.ground_df = pd.read_csv("../data/ground_truth.csv")
        self.max_df = self.extract_max_data()
        self.hottest_day, self.hottest_temperature = self.extract_hottest_day()
        self.coldest_day, self.coldest_temperature = self.extract_coldest_day()
        self.ground_truth = self.extract_filled_out_survey()

    def roll_data(self, window=20):
        """
        Rolls the data to get a rolling average of the data.
        Args:
            window (int): The window size for the rolling average (default: 20).
        Returns:
            pd.DataFrame: The rolled data.
        """
        numeric_cols = self.data.select_dtypes(include=[np.number])
        rolled_cols = numeric_cols.rolling(window).mean()
        return pd.concat([rolled_cols, self.data.select_dtypes(exclude=[np.number])], axis=1)

    def get_sensor_location(self):
        """
        Gets the sensor location for each sensor.
        Returns:
            dict: A dictionary of sensor locations.
        """
        return self.sensor_location

    def extract_day(self):
        """
        Extracts the day's data.
        Returns:
            pd.DataFrame: A DataFrame containing the day's data.
        """
        return self.data.between_time("5:00", "22:00")

    def extract_night(self):
        """
        Extracts the night's data.
        Returns:
            pd.DataFrame: A DataFrame containing the night's data.
        """
        df_night = self.data.between_time("22:00", "5:00")
        return df_night

    def extract_hottest_day(self):
        """
        Extracts the hottest day's data.'
        Returns:
            pd.DataFrame: A DataFrame containing the hottest day's data.
        """
        daily_mean_temperature = self.data["temperature"].resample("D").mean()
        hottest_day = pd.DataFrame(daily_mean_temperature.idxmax(), columns=["date"])
        hottest_temperature = pd.DataFrame(daily_mean_temperature.max(), columns=["temperature"])
        return hottest_day, hottest_temperature

    def extract_coldest_day(self):
        """
        Extracts the coldest day's data.'
        Returns:
            pd.DataFrame: A DataFrame containing the coldest day's data.
        """
        daily_mean_temperature = self.data["temperature"].resample("D").mean()
        coldest_day = pd.DataFrame(daily_mean_temperature.idxmin(), columns=["date"])
        coldest_temperature = pd.DataFrame(daily_mean_temperature.min(), columns=["temperature"])
        return coldest_day, coldest_temperature

    def extract_max_data(self):
        """
        Extracts the maximum values for each sensor for each day.
        Returns:
            pd.DataFrame: A DataFrame containing the max values for each sensor.
        """
        max_dict_light = self.extract_max_dictionary(self.sensor_dict, ["light"], self.num_days, self.location)
        max_dict_temp = self.extract_max_dictionary(self.sensor_dict, ["temperature"], self.num_days, self.location)
        max_light_df = pd.DataFrame(max_dict_light, index=["sensor", "date", "time", "timestamp", "value", "location"])
        max_temp_df = pd.DataFrame(max_dict_temp, index=["sensor", "date", "time", "timestamp", "value", "location"])
        names = ["max_light", "max_temperature"]
        for n, df1 in enumerate((max_light_df, max_temp_df)):
            new_columns = pd.MultiIndex.from_tuples(
                [(names[n], int(name.split("_")[1]), date) for name, date in df1.columns],
                names=[names[n], "sensor", "time"])
            df1.columns = new_columns
        max_df = max_light_df.join(max_temp_df)
        max_df.at["measurement", "max_light"] = "light"
        max_df.at["measurement", "max_temperature"] = "temperature"
        max_df = max_df.T
        return max_df

    def extract_max_dictionary(self, sensor_dict, cols_to_plot, num_days, loc):
        """
        Extracts the maximum values for each sensor and location.

        Args:
            sensor_dict (dict): A dictionary containing the sensors to plot.
            cols_to_plot (list): A list of columns to plot.
            num_days (int): The number of days to plot.
            loc (list): The location to plot.
        Returns:
            dict: A dictionary containing the max values for each sensor.
        """
        max_dict = {}
        end_date = pd.Timestamp(year=2023, month=10, day=30).normalize() - timedelta(days=1)
        max_value = 0
        df = self.data
        if isinstance(loc, str):
            loc = [loc]
        for loc_val in loc:
            for subtitle, sensors in sensor_dict.items():
                columns = [(col, f"{col}_{sensor}") for sensor in sensors for col in cols_to_plot]
                location_columns = [("location", f"location_{sensor}") for sensor in sensors]
                try:
                    data = df[columns + location_columns]
                except KeyError:
                    print(f"No weather_data for {columns[0][1]}")
                    continue
                if num_days is not None:
                    start_date = end_date - timedelta(days=num_days - 1)
                    data = data[(data.index >= start_date) & (data.index <= end_date)]
                for sensor in sensors:
                    sensor_location_col = ("location", f"location_{sensor}")
                    location = df[sensor_location_col].iloc[0]
                    if loc_val in location:
                        for col in cols_to_plot:
                            col_name = (col, f"{col}_{sensor}")
                            for day in range(num_days):
                                day_data = data[data.index.date == (end_date - timedelta(days=day)).date()]
                                try:
                                    max_point = max(day_data[col_name])
                                except ValueError:
                                    max_point = 0
                                try:
                                    min_point = min(day_data[col_name])
                                except ValueError:
                                    min_point = 0
                                if max_point != min_point:
                                    max_points = day_data[day_data[col_name] == max_point]
                                    if len(max_points) > 0:
                                        x = max_points.index[0]
                                        x_time = x.strftime("%H:%M")
                                        x_date = x.strftime("%m-%d")
                                        x_timestamp = x.strftime("%Y-%m-%d %H:%M")
                                        max_dict[col_name[1], x_date] = (
                                            sensor, x_date, x_time, x_timestamp, max_point, loc_val)
                                        df.loc[x, col_name] = max_point
                                        max_value = max(max_value, max_point)
        return max_dict

    def extract_filled_out_survey(self):
        """
        Extracts the filled out survey data.
        Returns:
            pd.DataFrame: A DataFrame containing the filled out survey data.
        """
        ground_df = self.ground_df[self.ground_df["did_survey"]]
        return ground_df

    def add_cardinal_directions_and_place(self):
        """
        Adds the cardinal directions and place for each sensor.
        Returns:
            pd.DataFrame: A DataFrame containing the cardinal directions and place for each sensor.
        """
        for name, sensor_group in self.sensor_dict.items():
            for sensor in sensor_group:
                filtered_rows = self.ground_df[self.ground_df["fyta_sensors"].str.contains(sensor)]
                compass_degree = filtered_rows["compass_degree"].iloc[0]
                self.max_df.loc[self.max_df["sensor"] == sensor, "compass_degree"] = compass_degree
        for sen in self.max_df["sensor"]:
            for key, value in self.sensor_dict.items():
                for val in value:
                    if val == sen:
                        self.max_df.loc[self.max_df["sensor"] == sen, "place"] = key
        return self.max_df

    def add_boum_temperature_values(self):
        """
        Adds the boum temperature values for each sensor.
        Returns:
            pd.DataFrame: A DataFrame containing the boum temperature values for each sensor.
        """
        df_day = self.extract_day()
        df_night = self.extract_night()
        for i in range(len(df_day["deviceId_boum"].iloc[0])):
            boum_id = df_day["deviceId_boum"].iloc[0][i]
            if boum_id in self.ground_df["deviceId_boum"].values:
                short_id = boum_id[:8]
                mean_temperature_day = df_day["temperature_boum"][f"temperature_boum_{short_id}"].mean()
                min_temperature_day = df_day["temperature_boum"][f"temperature_boum_{short_id}"].min()
                max_temperature_day = df_day["temperature_boum"][f"temperature_boum_{short_id}"].max()
                self.ground_df.loc[
                    self.ground_df["deviceId_boum"] == boum_id, "average_temperature_day"] = mean_temperature_day
                self.ground_df.loc[
                    self.ground_df["deviceId_boum"] == boum_id, "min_temperature_day"] = min_temperature_day
                self.ground_df.loc[
                    self.ground_df["deviceId_boum"] == boum_id, "max_temperature_day"] = max_temperature_day
        for i in range(len(df_day["deviceId_boum"].iloc[0])):
            boum_id = df_day["deviceId_boum"].iloc[0][i]
            if boum_id in self.ground_df["deviceId_boum"].values:
                short_id = boum_id[:8]
                mean_temperature_night = df_night["temperature_boum"][f"temperature_boum_{short_id}"].mean()
                min_temperature_night = df_night["temperature_boum"][f"temperature_boum_{short_id}"].min()
                max_temperature_night = df_night["temperature_boum"][f"temperature_boum_{short_id}"].max()
                self.ground_df.loc[
                    self.ground_df["deviceId_boum"] == boum_id, "average_temperature_night",] = mean_temperature_night
                self.ground_df.loc[
                    self.ground_df["deviceId_boum"] == boum_id, "min_temperature_night"] = min_temperature_night
                self.ground_df.loc[
                    self.ground_df["deviceId_boum"] == boum_id, "max_temperature_night"] = max_temperature_night
        for i in range(len(df_day["deviceId_boum"].iloc[0])):
            boum_id = df_day["deviceId_boum"].iloc[0][i]
            if boum_id in self.ground_df["deviceId_boum"].values:
                short_id = boum_id[:8]
                mean_temperature = self.data["temperature_boum"][f"temperature_boum_{short_id}"].mean()
                min_temperature = self.data["temperature_boum"][f"temperature_boum_{short_id}"].min()
                max_temperature = self.data["temperature_boum"][f"temperature_boum_{short_id}"].max()
                self.ground_df.loc[self.ground_df["deviceId_boum"] == boum_id, "average_temperature"] = mean_temperature
                self.ground_df.loc[self.ground_df["deviceId_boum"] == boum_id, "min_temperature"] = min_temperature
                self.ground_df.loc[self.ground_df["deviceId_boum"] == boum_id, "max_temperature"] = max_temperature
        self.extract_filled_out_survey()
        return self.ground_df

    def extract_max_temperature_and_light(self):
        """
        Extracts the max temperature and light for each sensor.
        Returns:
            pd.DataFrame: A DataFrame containing the max temperature and light for each sensor.
        """
        max_temp = self.max_df.loc["max_temperature"]
        max_light = self.max_df.loc["max_light"]
        return max_temp, max_light

    def get_sensor_dict(self):
        """
        Returns a dictionary containing the sensor IDs and their corresponding device IDs.
        Returns:
            dict: A dictionary containing the sensor IDs and their corresponding device IDs.
        """
        return self.sensor_dict

    def get_device_dict(self):
        """
        Returns a dictionary containing the device IDs and their corresponding sensor IDs.
        Returns:
            dict: A dictionary containing the device IDs and their corresponding sensor IDs.
        """
        return self.device_dict

    def calculate_mean_temperature(self):
        """
        Calculates the mean temperature for each sensor.
        Returns:
            pd.DataFrame: A DataFrame containing the mean temperature for each sensor.
        """
        max_temp, max_light = self.extract_max_temperature_and_light()
        sensor_list = set(max_light.sensor)
        for sensor in sensor_list:
            max_light.loc[max_light["sensor"] == sensor, "value"] = max_light.loc[
                max_light["sensor"] == sensor, "value"].mean()
            max_temp.loc[max_temp["sensor"] == sensor, "value"] = max_temp.loc[
                max_temp["sensor"] == sensor, "value"].mean()
        return max_temp, max_light

    def find_coldest_and_hottest_balcony_sensors(self):
        """
        Finds the coldest and hottest balcony sensors.
        Returns:
            pd.DataFrame: A DataFrame containing the coldest and hottest balcony sensors.
        """
        temperature_dict = {}
        for i in self.data.temperature:
            temperature_mean = self.data["temperature"][i].mean().round(1)
            temperature_max = self.data["temperature"][i].max().round(1)
            temperature_min = self.data["temperature"][i].min().round(1)
            sensor_name = str(i)[12:]
            temperature_dict[sensor_name] = (temperature_min, temperature_max, temperature_mean,)
        light_dict = {}
        for i in self.data.light:
            light_min = self.data["light"][i].min().round(1)
            light_max = self.data["light"][i].max().round(1)
            light_mean = self.data["light"][i].mean().round(1)
            sensor_name = str(i)[6:]
            light_dict[sensor_name] = light_min, light_max, light_mean
        balcony_temperature_df = pd.DataFrame(temperature_dict, index=["min", "max", "mean"])
        balcony_light_df = pd.DataFrame(light_dict, index=["min", "max", "mean"])
        balcony_temperature_df = balcony_temperature_df.T
        balcony_light_df = balcony_light_df.T
        for idx in balcony_temperature_df.index:
            for key, value in self.sensor_dict.items():
                for val in value:
                    if val == idx:
                        balcony_temperature_df.loc[balcony_temperature_df.index == idx, "place"] = key
        for idx in balcony_light_df.index:
            for key, value in self.sensor_dict.items():
                for val in value:
                    if val == idx:
                        balcony_light_df.loc[balcony_light_df.index == idx, "place"] = key
        result_df_temperature = (balcony_temperature_df.groupby("place").agg(["mean"]).round(1))
        result_df_light = balcony_light_df.groupby("place").agg(["mean"]).round(1)
        max_mean_temp_place = result_df_temperature["mean"].idxmax()
        result_df_temperature["mean"].max()
        result_df_light["mean"].idxmax()
        result_df_light["mean"].max()
        min_mean_temp_place = result_df_temperature["mean"].idxmin()
        result_df_temperature["mean"].min()
        result_df_light["mean"].idxmin()
        result_df_light["mean"].min()
        coldest_balcony_sensors = self.sensor_dict[min_mean_temp_place[0]]
        hottest_balcony_sensors = self.sensor_dict[max_mean_temp_place[0]]
        return coldest_balcony_sensors, hottest_balcony_sensors

    def find_hottest_and_coldest_balconies(self, coldest_balcony_sensors, hottest_balcony_sensors):
        """
        Finds the hottest and coldest balconies.
        Args:
            coldest_balcony_sensors (list): A list containing the coldest balcony sensors.
            hottest_balcony_sensors (list): A list containing the hottest balcony sensors.
        Returns:
            pd.DataFrame: A DataFrame containing the hottest and coldest balconies.
        """
        coldest_balcony = pd.DataFrame()
        for sensor in coldest_balcony_sensors:
            for temp_measurement in self.data.temperature:
                if sensor in temp_measurement:
                    coldest_balcony[temp_measurement] = self.data["temperature"][temp_measurement]
        base_names = coldest_balcony.columns.str.rsplit("_", n=1).str[0]
        columns = pd.MultiIndex.from_arrays([base_names, coldest_balcony.columns])
        coldest_balcony.columns = columns
        coldest_balcony = coldest_balcony.groupby(level=0, axis=1).apply(lambda x: x.select_dtypes(include=np.number))
        coldest_balcony.columns = coldest_balcony.columns.droplevel(0)

        hottest_balcony = pd.DataFrame()
        for sensor in hottest_balcony_sensors:
            for temp_measurement in self.data.temperature:
                if sensor in temp_measurement:
                    hottest_balcony[temp_measurement] = self.data["temperature"][temp_measurement]
        base_names = hottest_balcony.columns.str.rsplit("_", n=1).str[0]
        columns = pd.MultiIndex.from_arrays([base_names, hottest_balcony.columns])
        hottest_balcony.columns = columns
        hottest_balcony = hottest_balcony.groupby(level=0, axis=1).apply(lambda x: x.select_dtypes(include=np.number))
        hottest_balcony.columns = hottest_balcony.columns.droplevel(0)
        return coldest_balcony, hottest_balcony

    def find_hottest_and_coldest_day(self, coldest_balcony_sensors, hottest_balcony_sensors, coldest_balcony,
                                     hottest_balcony):
        """
        Finds the hottest and coldest balconies.
        Args:
            coldest_balcony_sensors (list): List of sensor names for the coldest balconies.
            hottest_balcony_sensors (list): List of sensor names for the hottest balconies.
            coldest_balcony (pd.DataFrame): DataFrame containing the coldest balconies.
            hottest_balcony (pd.DataFrame): DataFrame containing the hottest balconies.
        Returns:
            pd.DataFrame: A DataFrame containing the hottest and coldest balconies.
        """
        list(coldest_balcony["temperature"].columns)
        list(hottest_balcony["temperature"].columns)
        hottest_day = pd.DataFrame(self.hottest_day)
        hottest_day.columns = ["day"]
        hottest_day.index.name = "sensor"
        sensor_columns = [f"temperature_{sensor}" for sensor in coldest_balcony_sensors]
        filtered_temperature_cold_df = self.data["temperature"][sensor_columns]
        day_to_plot_hot = hottest_day[hottest_day.index == filtered_temperature_cold_df.columns[0]]
        coldest_day = pd.DataFrame(self.coldest_day)
        coldest_day.columns = ["day"]
        coldest_day.index.name = "sensor"
        sensor_columns = [f"temperature_{sensor}" for sensor in hottest_balcony_sensors]
        filtered_temperature_hot_df = self.data["temperature"][sensor_columns]
        day_to_plot_cold = coldest_day[coldest_day.index == filtered_temperature_hot_df.columns[0]]
        day_to_plot_hot = day_to_plot_hot["day"].iloc[0].date()
        day_to_plot_cold = day_to_plot_cold["day"].iloc[0].date()
        day_to_plot_hot = day_to_plot_hot.strftime("%Y-%m-%d")
        day_to_plot_cold = day_to_plot_cold.strftime("%Y-%m-%d")
        return day_to_plot_cold, day_to_plot_hot, filtered_temperature_cold_df, filtered_temperature_hot_df,

    def extract_extremes_to_plot(self):
        """
        Extracts the data for the coldest and hottest day for each balcony and returns them as a tuple of dataframes
        Returns:
            pd.DataFrame: A DataFrame containing the hottest and coldest balconies.
        """
        (coldest_balcony_sensors, hottest_balcony_sensors) = self.find_coldest_and_hottest_balcony_sensors()
        coldest_balcony, hottest_balcony = self.find_hottest_and_coldest_balconies(coldest_balcony_sensors,
                                                                                   hottest_balcony_sensors)
        (day_to_plot_cold, day_to_plot_hot, filtered_temperature_cold_df,
         filtered_temperature_hot_df,) = self.find_hottest_and_coldest_day(coldest_balcony_sensors,
                                                                           hottest_balcony_sensors, coldest_balcony,
                                                                           hottest_balcony)
        return (
        day_to_plot_hot, day_to_plot_cold, filtered_temperature_cold_df, filtered_temperature_hot_df, hottest_balcony,
        coldest_balcony,)

    def get_tank_sensor_list(self):
        """
        Returns the list of tank sensors.
        Returns:
            list: A list of tank sensors.
        """
        return self.tank_sensor_list

    def get_sun_tank_sensor_list(self):
        """
        Returns the list of sun and tank sensors.
        Returns:
            list: A list of sun and tank sensors.
        """
        return self.sun_tank_sensor_list

    def get_orientation_dict(self):
        """
        Returns the dictionary of orientations.
        Returns:
            dict: A dictionary of orientations.
        """
        return self.orientation_dict

    def get_device_list(self):
        """
        Returns the list of devices.
        Returns:
            list: A list of devices.
        """
        return self.device_list

    def extract_max_daily_values_fyta(self, sensor_list):
        """
        Extracts the maximum daily values for a given list of sensors.
        Args:
            sensor_list (list): A list of sensors.
        Returns:
            tuple: A tuple containing the maximum daily values for each sensor.
        """
        max_values_df = pd.DataFrame(columns=["sensor", "max_light_time", "max_temperature_time", "orientation"])
        max_values_list = []
        for sensor in sensor_list:
            light_col = self.data["light"][f"light_{sensor}"]
            temperature_col = self.data["temperature"][f"temperature_{sensor}"]
            for key, value in self.orientation_dict.items():
                sensor = str(sensor)
                if sensor in value:
                    orientation = key
            max_light_index = light_col.groupby(light_col.index.date).idxmax()
            max_temperature_index = temperature_col.groupby(temperature_col.index.date).idxmax()

            max_light_times = max_light_index.dt.time
            max_temperature_times = max_temperature_index.dt.time
            sensor_results = pd.DataFrame({"sensor": [sensor] * len(max_light_times), "max_light_time": max_light_times,
                                           "max_temperature_time": max_temperature_times, "orientation": orientation})
            max_values_list.append(sensor_results)
            max_values_df = pd.concat(max_values_list, ignore_index=True)
        return max_values_df

    def extract_max_daily_values_boum(self, device_list):
        """
        Extracts the maximum daily values for a given list of devices.
        Args:
            device_list (list): A list of devices.
        Returns:
            tuple: A tuple containing the maximum daily values for each device.
        """
        max_values_list = []
        for device in device_list:
            device_name = device[:8]
            input_current_col = self.data["inputCurrent_boum"][f"inputCurrent_boum_{device_name}"]
            temperature_boum_col = self.data["temperature_boum"][f"temperature_boum_{device_name}"]
            temperature_esp_col = self.data["temperatureEsp_boum"][f"temperatureEsp_boum_{device_name}"]
            for key, value in self.orientation_dict.items():
                device = str(device)
                if device in value:
                    orientation = key
            input_current_col = pd.to_datetime(input_current_col)
            temperature_boum_col = pd.to_datetime(temperature_boum_col)
            temperature_esp_col = pd.to_datetime(temperature_esp_col)
            if not input_current_col.empty:
                max_input_current_index = input_current_col.groupby(input_current_col.index.date).idxmax()
                max_input_current_times = max_input_current_index.dt.time
            else:
                max_input_current_times = []
            if not temperature_boum_col.empty:
                max_temperature_boum_index = temperature_boum_col.groupby(temperature_boum_col.index.date).idxmax()
                max_temperature_times = max_temperature_boum_index.dt.time
            else:
                max_temperature_times = []
            if not temperature_esp_col.empty:
                max_temperatureEsp_index = temperature_esp_col.groupby(temperature_esp_col.index.date).idxmax()
                max_temperatureEsp_times = max_temperatureEsp_index.dt.time
            else:
                max_temperatureEsp_times = []
            max_times_count = max(len(max_input_current_times), len(max_temperature_times),
                                  len(max_temperatureEsp_times))

            sensor_results = pd.DataFrame(
                {"sensor": [device] * max_times_count, "max_input_current_time_boum": max_input_current_times,
                 "max_temperature_time_boum": max_temperature_times,
                 "max_temperatureEsp_time_boum": max_temperatureEsp_times,
                 "orientation": [orientation] * max_times_count})

            max_values_list.append(sensor_results)

        return pd.concat(max_values_list, ignore_index=True)

# %%
