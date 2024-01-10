"""
This module contains a class for plotting data.
"""
import math
from datetime import timedelta, datetime

import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt


def set_color_palette(size):
    """
    Method to set the color palette.
    Args:
        size (int): Number of colors.
    Returns:
        list: Color palette.
    """
    return sns.color_palette("colorblind", n_colors=size)


class Plotter:
    """
    Class for plotting data.
    """

    def __init__(self):
        """
        Initializes the Plotter class.
        """
        self.location_styles = {"pot": ":", "sun": "-", "tank": "--", "temperature": "--", "light": "-"}
        self.date = pd.Timestamp(year=2023, month=10, day=30).strftime("%Y-%m-%d")
        self.end_date = pd.Timestamp(year=2023, month=10, day=30).normalize() - timedelta(days=1)
        self.sensor_dict = {"loc_1": ["21328", "21329", "21331"], "loc_0": ["14541", "21356", "14539"],
                            "loc_2": ["21335", "21332", "21334"], "loc_4": ["21349", "21350", "21351"],
                            "loc_9": ["21341", "21343"], "loc_6": ["21355", "21347", "21348"],
                            "loc_5": ["21337", "21338"], "loc_8": ["21326", "21327"],
                            "loc_3": ["21344", "21345", "21346"], "loc_7": ["21352", "21353", "21354"]}
        self.numerical_columns = ["latitude", "longitude", "floor", "pot_count", "rating_climate_user",
                                  "rating_user_tomato", "rating_user_basil", "min_temperature", "average_temperature",
                                  "max_temperature", "compass_degree"]

        self.sensor_id_dict = {"655c77c8-0b0f-47c7-9f6c-fe517756829e": ["21328", "21329", "21331"],
                               "13235f69-0f74-4ef7-955d-848e831ffc3c": ["14541", "21356", "14539"],
                               "a2146308-f5e9-4cfe-a8c5-7b84cb4f70af": ["21335", "21332", "21334"],
                               "2a650b37-9645-46e0-825e-4a5319c09b03": ["21349", "21350", "21351"],
                               "32a5c848-366d-4029-8861-9689acf35b85": ["21341", "21343"],
                               "188be60e-3894-4e80-8850-165ba1e0061c": ["21355", "21347", "21348"],
                               "a27e798c-e69c-4603-b720-d195be6c8623": ["21337", "21338"],
                               "64f7fddf-01ac-4826-aaab-fcf4232e5bc6": ["21326", "21327"],
                               "cc1b8cb9-cafb-4bcf-b346-f4009c0403c8": ["21344", "21345", "21346"],
                               "5fe95b01-dce7-4c29-aae6-a39009f9e166": ["21352", "21353", "21354"], }
        self.device_dict = {"loc_1": "655c77c8-0b0f-47c7-9f6c-fe517756829e",
                            "loc_0": "13235f69-0f74-4ef7-955d-848e831ffc3c",
                            "loc_2": "a2146308-f5e9-4cfe-a8c5-7b84cb4f70af",
                            "loc_4": "2a650b37-9645-46e0-825e-4a5319c09b03",
                            "loc_9": "32a5c848-366d-4029-8861-9689acf35b85",
                            "loc_6": "188be60e-3894-4e80-8850-165ba1e0061c",
                            "loc_5": "a27e798c-e69c-4603-b720-d195be6c8623",
                            "loc_8": "64f7fddf-01ac-4826-aaab-fcf4232e5bc6",
                            "loc_3": "cc1b8cb9-cafb-4bcf-b346-f4009c0403c8",
                            "loc_7": "5fe95b01-dce7-4c29-aae6-a39009f9e166", }
        self.cmap = "icefire"
        self.path = "../plots/"
        self.color = set_color_palette(10)
        self.sensor_location = {"tank": [21328, 21335, 14541, 21355, 21352, 21349, 21344, 21339],
                                "sun": [21329, 21332, 21356, 21347, 21337, 21353, 21350, 21326, 21345, 21341],
                                "pot": [21331, 21334, 14539, 21348, 21338, 21354, 21351, 21327, 21346, 21343]}

    def plot_one_plot(self, df, cols_to_plot, num_days, loc):
        """
        Method to plot data in one plot.

        Args:
            df (pd.DataFrame): Dataframe containing the data.
            cols_to_plot (list): List of columns to plot.
            num_days (int): Number of days to plot.
            loc (list): List of locations to plot.
        """
        num_cols = 3
        if isinstance(loc, str):
            loc = [loc]
        num_locations = len(loc)
        num_rows = math.ceil(num_locations / num_cols)
        fig, axs = plt.subplots(num_rows, num_cols, figsize=(24, 6 * num_rows))
        fig.suptitle("FYTA Sensor Data", fontsize=16)
        color_palette = sns.color_palette("colorblind", n_colors=len(self.sensor_dict))
        color_mapping = dict(zip(self.sensor_dict.keys(), color_palette))
        plt.tight_layout()
        max_value = 0
        for ax in axs.flat:
            ax.grid(True)
        for i, loc_val in enumerate(loc):
            for subtitle, sensors in self.sensor_dict.items():
                columns = [(col, f"{col}_{sensor}") for sensor in sensors for col in cols_to_plot]
                location_columns = [("location", f"location_{sensor}") for sensor in sensors]
                try:
                    data = df[columns + location_columns]
                except KeyError:
                    print(f"No weather_data for {columns[0][1]}")
                    continue
                if num_days is not None:
                    start_date = self.end_date - timedelta(days=num_days)
                    data = data[(data.index >= start_date) & (data.index <= self.end_date)]
                ax = (axs[i // num_cols, i % num_cols] if num_rows > 1 else axs[i % num_cols])
                ax.set_xlabel("Time", fontsize=12)
                ax.set_ylabel(f'{", ".join(cols_to_plot)} value', fontsize=12)
                ax.set_xticks(data.index[:: 5 * num_days])
                ax.set_xticklabels(data[:: 5 * num_days].index.strftime("%b-%d %H:%M"), rotation=90, fontsize=10, )
                legend_labels = set()
                for sensor in sensors:
                    sensor_location_col = ("location", f"location_{sensor}")
                    location = df[sensor_location_col].iloc[0]
                    if loc_val in location:
                        line_style = self.location_styles.get(location, "-")
                        color = color_mapping[subtitle]
                        for col in cols_to_plot:
                            col_name = (col, f"{col}_{sensor}")
                            for day in range(2, num_days):
                                day_data = data[data.index.date == (self.end_date - timedelta(days=day)).date()]
                                max_point = np.max(day_data[col_name])
                                min_point = np.min(day_data[col_name])
                                if max_point != min_point:
                                    max_points = day_data[day_data[col_name] == max_point]
                                    if len(max_points) > 0:
                                        x = max_points.index[0]
                                        x_time = x.strftime("%H:%M")
                                        ax.scatter(x, max_point, color=color)
                                        ax.text(x, max_point, x_time, color=color, fontsize=12, ha="center",
                                                va="center", linespacing=1.5,
                                                position=(x, max_point + (max_point / 30)))
                                        max_value = np.max(max_value, max_point)
                                    ax.plot(day_data.index, day_data[col_name], line_style, color=color,
                                            label=f"{col} ({location}), {subtitle}"
                                            if col_name not in legend_labels else "")
                                    legend_labels.add(col_name)
                        plt.ylim(0, max_value + 1)
        plt.subplots_adjust(top=0.90, bottom=0.1)
        plt.figlegend(loc="lower center", ncol=3, bbox_to_anchor=(0.5, -0.6), fontsize=12)
        plt.tight_layout()
        plt.savefig(
            f'{self.path}FYTA_Sensor_Data_one_{loc}_{cols_to_plot}_{pd.Timestamp.now().strftime("%Y-%m-%d")}.jpeg',
            bbox_inches="tight")
        plt.show()

    def plot_multiple_plots(self, df, cols_to_plot, num_days, loc):
        """
        Method to plot data in multiple plots.

        Args:
            df (pd.DataFrame): Dataframe containing the data.
            cols_to_plot (list): List of columns to plot.
            num_days (int): Number of days to plot.
            loc (list): List of locations to plot.
        """
        num_cols = 3
        if isinstance(loc, str):
            loc = [loc]
        num_plots = len(self.sensor_dict)
        num_rows = math.ceil(num_plots / num_cols)
        fig, axs = plt.subplots(num_rows, num_cols, figsize=(24, 12))
        fig.suptitle("FYTA Sensor Data", fontsize=20, y=1)
        plt.tight_layout()
        for i, (subtitle, sensors) in enumerate(self.sensor_dict.items()):
            ax1 = axs[int(i) // num_cols][i % num_cols]
            color_palette = sns.color_palette("colorblind", n_colors=len(cols_to_plot))
            color_mapping = dict(zip(list(cols_to_plot), color_palette))
            columns = [(col, f"{col}_{sensor}") for sensor in sensors for col in cols_to_plot]
            location_columns = [("location", f"location_{sensor}") for sensor in sensors]
            try:
                data = df[columns + location_columns]
            except KeyError:
                print(f"No weather_data for {columns[0][1]}")
                continue
            if num_days is not None:
                start_date = self.end_date - timedelta(days=num_days)
                data = data[(data.index >= start_date) & (data.index <= self.end_date)]
            for sensor in sensors:
                sensor_location_col = ("location", f"location_{sensor}")
                for col in cols_to_plot:
                    col_name = (col, f"{col}_{sensor}")
                    location = df[sensor_location_col].iloc[0]
                    if loc[0] in location:
                        line_style = self.location_styles[location]
                    else:
                        continue
                    color = color_mapping[col]
                    legend_labels = set()
                    if col == "temperature":
                        ax1.set_xlabel("Time", fontsize=12)
                        ax1.set_ylabel("Temperature [°C]", color=color)
                        ax1.tick_params(axis="y", labelcolor=color)
                        ax1.set_yticks(range(0, 51, 5))
                        ax1.set_ylim(0, 50)
                        ax1.set_xticks(data.index[:: 5 * num_days])
                        ax1.set_xticklabels(data[:: 5 * num_days].index.strftime("%b-%d %H:%M"), rotation=90,
                                            fontsize=12, )
                        for day in range(2, num_days):
                            day_data = data[data.index.date == (self.end_date - timedelta(days=day)).date()]
                            max_point = np.max(day_data[col_name])
                            min_point = np.min(day_data[col_name])
                            if max_point != min_point:
                                max_points = day_data[day_data[col_name] == max_point]
                                if len(max_points) > 0:
                                    x = max_points.index[0]
                                    x_time = x.strftime("%H:%M")
                                    ax1.scatter(x, max_point, color=color)
                                    ax1.text(x, max_point, x_time, color=color, fontsize=15, ha="center", va="center",
                                             linespacing=1.5, position=(x, max_point + (max_point / 10)))
                                ax1.plot(day_data.index, day_data[col_name], line_style, color=color,
                                         label=f"{col} ({location})" if col_name not in legend_labels else "")
                                legend_labels.add(col_name)
                    elif col == "light":
                        ax2 = ax1.twinx()
                        ax2.set_ylabel("Light Intensity", color=color, labelpad=20)
                        ax2.tick_params(axis="y", labelcolor=color)
                        ax2.set_yticks(range(0, 3001, 600))
                        ax2.set_ylim(0, 3000)
                        for day in range(2, num_days):
                            day_data = data[data.index.date == (self.end_date - timedelta(days=day)).date()]
                            max_point = np.max(day_data[col_name])
                            min_point = np.min(day_data[col_name])
                            if max_point != min_point:
                                max_points = day_data[day_data[col_name] == max_point]
                                if len(max_points) > 0:
                                    x = max_points.index[0]
                                    x_time = x.strftime("%H:%M")
                                    ax2.scatter(x, max_point, color=color)
                                    ax2.text(x, max_point, x_time, color=color, fontsize=15, ha="center", va="center",
                                             linespacing=1.5, position=(x, max_point + (max_point / 10)))
                                ax2.plot(day_data.index, day_data[col_name], line_style, color=color,
                                         label=f"{col} ({location})" if col_name not in legend_labels else "")
                                legend_labels.add(col_name)
                                ax2.legend(frameon=False, loc="upper right")
            ax1.grid(True)
            ax1.set_title(subtitle)
            ax1.legend(frameon=False, loc="upper left")
        if num_plots < num_rows * num_cols:
            for i in range(num_plots, num_rows * num_cols):
                ax = axs[i // num_cols, i % num_cols]
                fig.delaxes(ax)
        plt.tight_layout()
        plt.savefig(
            f'{self.path}FYTA_Sensor_Data_multiple_{cols_to_plot}_{loc}_'
            f'{pd.Timestamp.now().strftime("%Y-%m-%d")}.jpeg',
            bbox_inches="tight")
        plt.show()

    def plot_selected_sensor_data(self, df, cols_to_plot, sensor_key, num_days=2):
        """
        Method to plot selected sensor data.

        Args:
            df (pd.DataFrame): Dataframe containing the data.
            cols_to_plot (list): List of columns to plot.
            sensor_key (str): Sensor key to filter the data.
            num_days (int): Number of days to plot.
        """
        num_cols = 3
        if isinstance(sensor_key, str):
            sensor_key = [sensor_key]
        num_plots = len(sensor_key)
        num_rows = (num_plots + num_cols - 1) // num_cols
        fig, axs = plt.subplots(num_rows, num_cols, figsize=(24, 12))
        fig.suptitle("FYTA Sensor Data", fontsize=20, y=1)
        location_mapping = {}
        color_palette = sns.color_palette("colorblind", n_colors=len(cols_to_plot))
        color_mapping = dict(zip(list(cols_to_plot), color_palette))
        plt.tight_layout()
        for i, (subtitle, sensors) in enumerate(self.sensor_dict.items()):
            if subtitle not in sensor_key:
                continue
            if num_rows > 1:
                row, col = np.unravel_index(int(i), (num_rows, num_cols))
                ax1 = axs[row, col]
                ax2 = ax1.twinx()
            else:
                ax1 = axs[i]
            columns = [(col, f"{col}_{sensor}") for sensor in sensors for col in cols_to_plot]
            location_columns = [("location", f"location_{sensor}") for sensor in sensors]
            try:
                data = df[columns + location_columns]
            except KeyError:
                print(f"No weather_data for {columns[0][1]}")
                continue
            if num_days is not None:
                end_date = pd.Timestamp(year=2023, month=10, day=30).normalize() - pd.DateOffset(days=1)
                start_date = end_date - pd.DateOffset(days=num_days - 1)
                data = data[(data.index >= start_date) & (data.index <= end_date)]
            ax1.set_xlabel("Time", fontsize=12)
            ax1.set_xticks(data.index[:: 5 * num_days])
            ax1.set_xticklabels(data[:: 5 * num_days].index.strftime("%b-%d %H:%M"), rotation=90, fontsize=12)
            for sensor in sensors:
                if sensor not in sensor_key:
                    continue
                sensor_location_col = ("location", f"location_{sensor}")
                location = (location_mapping.get(sensor) or df[sensor_location_col].iloc[0])
                location_mapping[sensor] = location
                line_style = (self.location_styles[location] if len(cols_to_plot) > 1 else "-")
                legend_labels = set()
                day_data = data[data.index.date == (end_date - pd.DateOffset(days=num_days)).date()]
                for col in cols_to_plot:
                    if col == "temperature":
                        col_name = (col, f"{col}_{sensor}")
                        max_point = np.max(day_data[col_name])
                        min_point = np.min(day_data[col_name])
                        if max_point != min_point:
                            max_points = day_data[day_data[col_name] == max_point]
                            if len(max_points) > 0:
                                x = max_points.index[0]
                                x_time = x.strftime("%H:%M")
                                ax1.scatter(x, max_point, color=color_mapping[col])
                                ax1.text(x, max_point, x_time, color=color_mapping[col], fontsize=15, ha="center",
                                         va="center", linespacing=1.5, position=(x, max_point + (max_point / 10)))
                                ax1.plot(day_data.index, day_data[col_name], line_style, color=color_mapping[col],
                                         label=f"{col} ({location})" if col_name not in legend_labels else "")
                                legend_labels.add(col_name)
                    elif col == "light":
                        col_name = (col, f"{col}_{sensor}")
                        max_point = np.max(day_data[col_name])
                        min_point = np.min(day_data[col_name])
                        if max_point != min_point:
                            max_points = day_data[day_data[col_name] == max_point]
                            if len(max_points) > 0:
                                x = max_points.index[0]
                                x_time = x.strftime("%H:%M")
                                ax2.scatter(x, max_point, color=color_mapping[col])
                                ax2.text(x, max_point, x_time, color=color_mapping[col], fontsize=15, ha="center",
                                         va="center", linespacing=1.5, position=(x, max_point + (max_point / 10)))
                                ax2.plot(day_data.index, day_data[col_name], line_style, color=color_mapping[col],
                                         label=f"{col} ({location})" if col_name not in legend_labels else "")
                                legend_labels.add(col_name)
            ax1.grid(True)
            # ax1.legend(frameon=False)
            ax1.set_title(subtitle)
        if num_plots < num_rows * num_cols:
            for i in range(num_plots, num_rows * num_cols):
                fig.delaxes(axs.flatten()[i])
        plt.tight_layout()
        plt.savefig(
            f'{self.path}FYTA_Sensor_Data_selected_sensor{cols_to_plot}_{sensor_key}_'
            f'{pd.Timestamp.now().strftime("%Y-%m-%d")}.jpeg',
            bbox_inches="tight")
        plt.show()

    def plot_multiple_days(self, df, sensor_key, cols_to_plot, num_days, loc):
        """
        Plots multiple days of sensor data for a given sensor key.
        Args:
            df (pd.DataFrame): Dataframe containing the data.
            sensor_key (str): Sensor key to filter the data.
            cols_to_plot (list): List of columns to plot.
            num_days (int): Number of days to plot.
            loc (str): Location to filter the data.
        """
        num_cols = 3
        if isinstance(loc, str):
            loc = [loc]
        num_plots = num_days
        num_rows = (num_plots + num_cols - 1) // num_cols
        fig, axs = plt.subplots(num_rows, num_cols, figsize=(24, 12))
        fig.suptitle("FYTA Sensor Data", fontsize=20, y=1)
        color_palette = sns.color_palette("colorblind", n_colors=len(cols_to_plot))
        color_mapping = dict(zip(list(cols_to_plot), color_palette))
        plt.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.9, wspace=0.2, hspace=0.3)
        for day in range(2, num_days):
            end_date = pd.Timestamp(year=2023, month=10, day=30).normalize() - pd.DateOffset(days=1)
            for i, (subtitle, sensors) in enumerate(self.sensor_dict.items()):
                if subtitle not in sensor_key:
                    continue
                ax1 = axs[day // num_cols, day % num_cols]
                columns = [(col, f"{col}_{sensor}") for sensor in sensors for col in cols_to_plot]
                location_columns = [("location", f"location_{sensor}") for sensor in sensors]
                try:
                    data = df[columns + location_columns]
                except KeyError:
                    print(f"No weather_data for {columns[0][1]}")
                    continue
                ax1.set_xlabel("Time", fontsize=12)
                ax1.set_xticks(data.index[::7])
                ax1.set_xticklabels(data[::7].index.strftime("%H:%M"), rotation=90, fontsize=12)
                day_data = data[data.index.date == (end_date - pd.DateOffset(days=day)).date()]
                if not day_data.index.empty:
                    ax1.set_title(f'{subtitle} - {day_data.index[0].strftime("%Y-%m-%d")}')
                for sensor in sensors:
                    sensor_location_col = ("location", f"location_{sensor}")
                    legend_labels = set()
                    for key, value in self.sensor_id_dict.items():
                        if sensor in value:
                            boum_id = key
                    for col in cols_to_plot:
                        col_name = (col, f"{col}_{sensor}")
                        location = df[sensor_location_col].iloc[0]
                        if location in loc:
                            line_style = self.location_styles[location]
                        else:
                            continue
                        color = color_mapping[col]
                        if not day_data.empty:
                            if col == "temperature":
                                temperature_data = day_data[("temperature", f"temperature_{sensor}")]
                                ax1.plot(temperature_data.index, temperature_data, line_style, color=color,
                                         label=f"{col} ({location})" if col_name not in legend_labels else "")
                                ax1.set_ylabel("Temperature [°C]", color=color)
                                ax1.tick_params(axis="y", labelcolor=color)
                                ax1.set_yticks(range(0, 51, 5))
                                ax1.set_ylim(0, 50)
                                legend_labels.add(col_name)
                            elif col == "light":
                                ax2 = ax1.twinx()
                                light_data = day_data[("light", f"light_{sensor}")]
                                ax2.plot(light_data.index, light_data, line_style, color=color,
                                         label=f"{col} ({location})" if col_name not in legend_labels else "")
                                ax2.set_ylabel("Light Intensity", color=color)
                                ax2.tick_params(axis="y", labelcolor=color)
                                ax2.set_yticks(range(0, 3501, 600))
                                ax2.set_ylim(0, 3500)
                                legend_labels.add(col_name)
                boum_id = boum_id[:-28]
                direct_normal_data = df["direct_normal_irradiance"][f"direct_normal_irradiance_{boum_id}"]
                if not day_data.index.empty:
                    day_direct_normal_data = direct_normal_data[(direct_normal_data.index >= day_data.index[0]) & (
                            direct_normal_data.index <= day_data.index[-1])]
                    ax2.plot(day_direct_normal_data.index, day_direct_normal_data, ".-", color="tab:grey",
                             label="Direct Normal Irradiance [W/m^2]")
                ax2.legend(loc="upper right", frameon=False)
                ax1.legend(loc="upper left", frameon=False)
        if num_plots < num_rows * num_cols:
            for i in range(num_plots, num_rows * num_cols):
                fig.delaxes(axs.flatten()[i])
        plt.tight_layout()
        plt.savefig(
            f'{self.path}multiple_days_{sensor_key}_{loc}_{cols_to_plot}_{pd.Timestamp.now().strftime("%Y-%m-%d")}.png')
        plt.show()

    def plot_temperature_data(self, ax, temperature_data, day_to_plot_datetime, title):
        """
        Plots temperature data for a given day.
        Args:
            ax (matplotlib.axes.Axes): Axes to plot on.
            temperature_data (pd.DataFrame): Dataframe containing the data.
            day_to_plot_datetime (pd.Timestamp): Timestamp of the day to plot.
            title (str): Title of the plot.
        """
        temperature_data_to_plot = temperature_data[
            (temperature_data.index > day_to_plot_datetime - pd.Timedelta(days=0)) & (
                    temperature_data.index < day_to_plot_datetime + pd.Timedelta(days=1))]
        lines = ax.plot(temperature_data_to_plot.index, temperature_data_to_plot.values)
        ax.set_xlabel("Time")
        ax.set_ylabel("Temperature")
        ax.set_title(title)
        ax.tick_params(axis="x", rotation=90)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
        ax.set_xticks(temperature_data_to_plot.index[::8])
        ax.set_ylim(5, 50)
        sensor_names = [col.split("_")[1] for col in temperature_data_to_plot.columns]
        ax.legend(lines, sensor_names, loc="upper left", fontsize="small", frameon=False)
        plt.tight_layout()
        plt.savefig(f'{self.path}temperature_{title}_{pd.Timestamp.now().strftime("%Y-%m-%d")}.png')
        plt.show()

    def plot_cardinal_and_max_values(self, max_temp, max_light):
        """
        Plots the cardinal and max values for a given day.
        Args:
            max_temp (pd.DataFrame): Dataframe containing the max temperature values.
            max_light (pd.DataFrame): Dataframe containing the max light values.
        """

        fig, axes = plt.subplots(1, 2, figsize=(12, 6))
        compass_degrees = np.arange(0, 360, 45)
        sns.scatterplot(x="compass_degree", y="value", hue="place", data=max_light, palette="tab10", legend="full",
                        alpha=0.5, ax=axes[0], style="location")
        axes[0].set_title("Max Light")
        axes[0].set_xticks(compass_degrees)
        sky_direction_labels = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
        axes[0].set_xticklabels([f"{deg}°\n{sky}" for deg, sky in zip(compass_degrees, sky_direction_labels)])
        axes[0].set_xlabel("Compass Degree")
        axes[0].set_ylabel("Value")
        axes[0].legend().set_visible(False)
        sns.scatterplot(x="compass_degree", y="value", hue="place", data=max_temp, palette="tab10", legend="full",
                        alpha=0.5, ax=axes[1], style="location")
        axes[1].set_title("Max Temperature")
        axes[1].set_xticks(compass_degrees)
        axes[1].set_xticklabels([f"{deg}°\n{sky}" for deg, sky in zip(compass_degrees, sky_direction_labels)])
        axes[1].set_xlabel("Compass Degree")
        axes[1].set_ylabel("Value")
        axes[1].legend().set_visible(False)
        axes[0].legend(loc="lower center", bbox_to_anchor=(0.5, -0.3), title="Legend", ncol=4)
        plt.tight_layout()
        plt.savefig(f'{self.path}compass_degree_temp_light_{pd.Timestamp.now().strftime("%Y-%m-%d")}.jpeg',
                    bbox_inches="tight", dpi=900)
        plt.show()

    def plot_survey_boxplots(self, ground_df):
        """
        Plots the boxplots.
        Args:
            ground_df (pd.DataFrame): Dataframe containing the data.
        """
        plt.figure(figsize=(12, 6))
        plt.suptitle("Boxplots", fontsize=16)
        sns.boxplot(x="location_type", y="average_temperature", hue="roof_type", data=ground_df,
                    palette=set_color_palette(5))
        plt.legend(loc="upper left", bbox_to_anchor=(1, 1), title="Roof Type")
        plt.xlabel("Location Type")
        plt.ylabel("Average Temperature [°C]")
        plt.tight_layout()
        plt.savefig(f"{self.path}boxplots.png", bbox_inches="tight")
        plt.show()

    def plot_survey_histograms(self, ground_df):
        """
        Plots the histograms.
        Args:
            ground_df (pd.DataFrame): Dataframe containing the data.
        """
        plt.figure(figsize=(12, 6))
        plt.suptitle("Histograms", fontsize=16)
        plt.subplot(121)
        self.plot_base(ground_df, "rating_user_tomato", "Rating User Tomato")
        plt.subplot(122)
        self.set_subplot_base(ground_df, "rating_user_basil", "Rating User Basil", "histograms.png")
        plt.figure(figsize=(12, 6))
        self.set_subplot_base(ground_df, "rating_climate_user", "Rating Climate User",
                              "histograms_climate_user.png")

    def set_subplot_base(self, ground_df, arg1, arg2, arg3):
        """
        Sets the subplot base for the histograms.
        Args:
            ground_df (pd.DataFrame): Dataframe containing the data.
            arg1 (str): Name of the column to plot.
            arg2 (str): Name of the plot.
            arg3 (str): Name of the file to save the plot.
        """
        self.plot_base(ground_df, arg1, arg2)
        plt.tight_layout()
        plt.savefig(f"{self.path}{arg3}", bbox_inches="tight")
        plt.show()

    @staticmethod
    def plot_base(ground_df, arg1, label):
        """
        Sets the base for the histograms.
        Args:
            ground_df (pd.DataFrame): Dataframe containing the data.
            arg1 (str): Name of the column to plot.
            label (str): Name of the plot.
        """
        sns.histplot(ground_df[arg1], label=label)
        plt.xlabel("Rating")

    def plot_survey_kde_plots(self, ground_df):
        """
        Plots the kde plots.
        Args:
            ground_df (pd.DataFrame): Dataframe containing the data.
        """
        plt.figure(figsize=(12, 6))
        plt.suptitle("KDE Plots", fontsize=16)
        sns.kdeplot(data=ground_df, x="average_temperature", fill=True, label="Average Temperature")
        sns.kdeplot(data=ground_df, x="min_temperature", fill=True, label="Min Temperature")
        sns.kdeplot(data=ground_df, x="max_temperature", fill=True, label="Max Temperature")
        plt.xlabel("Temperature [°C]")
        plt.legend(["Average Temperature", "Min Temperature", "Max Temperature"])
        plt.tight_layout()
        plt.savefig(f"{self.path}kde_plots.png", bbox_inches="tight")
        plt.show()

    def plot_survey_heatmaps(self, ground_df):
        """
        Plots the heatmaps.
        Args:
            ground_df (pd.DataFrame): Dataframe containing the data.
        """
        plt.figure(figsize=(12, 12))
        plt.suptitle("Heatmaps", fontsize=16)
        plt.subplot(221)
        sns.heatmap(ground_df[self.numerical_columns].corr(), annot=True, cmap=self.cmap)
        plt.title("All Numerical Columns Correlation")
        plt.subplot(222)
        selected_corr_columns = ["average_temperature", "min_temperature", "max_temperature", "compass_degree"]
        sns.heatmap(ground_df[selected_corr_columns].corr(), annot=True, cmap=self.cmap)
        plt.title("Selected Columns Correlation")
        plt.subplot(223)
        contingency_table = pd.crosstab(ground_df["roof_type"], ground_df["location_type"])
        sns.heatmap(contingency_table, annot=True, cmap=self.cmap)
        plt.title("Roof Type vs. Location Type")
        plt.subplot(224)
        columns_of_interest = ["orientation_balcony_short", "sunshine_window_user"]
        selected_data = ground_df[columns_of_interest].dropna(subset=columns_of_interest)
        contingency_table = pd.crosstab(selected_data["orientation_balcony_short"],
                                        selected_data["sunshine_window_user"], rownames=["Balcony Orientation"],
                                        colnames=["Sunshine Window User"])
        sns.heatmap(contingency_table, annot=True, cmap=self.cmap)
        plt.title("Balcony Orientation vs. Sunshine Window User")
        plt.subplots_adjust(wspace=0.5, hspace=0.5)
        plt.tight_layout()
        plt.savefig(f"{self.path}heatmaps.png", bbox_inches="tight")
        plt.show()

    def plot_survey_scatterplots(self, ground_df):
        """
        Plots the scatterplots.
        Args:
            ground_df (pd.DataFrame): Dataframe containing the data.
        """
        plt.figure(figsize=(12, 6))
        plt.suptitle("Scatterplots", fontsize=16)
        sns.scatterplot(x="compass_degree", y="average_temperature", data=ground_df, hue="tank_position",
                        style="tank_location", palette=set_color_palette(5))
        plt.legend(loc="upper left", bbox_to_anchor=(1, 1), title="Tank position")
        plt.xlabel("Compass Degree")
        plt.ylabel("Average Temperature [°C]")
        plt.tight_layout()
        plt.savefig(f"{self.path}scatterplots.png", bbox_inches="tight")
        plt.show()

    def plot_survey_countplots(self, ground_df):
        """
        Plots the countplots.
        Args:
            ground_df (pd.DataFrame): Dataframe containing the data.
        """
        plt.figure(figsize=(12, 6))
        plt.suptitle("Countplots", fontsize=16)
        sns.countplot(x="location_type", hue="blinds_frequency", data=ground_df, palette=set_color_palette(5))
        plt.legend(loc="upper left", bbox_to_anchor=(1, 1), title="Blinds Frequency")
        plt.tight_layout()
        plt.savefig(f"{self.path}_countplots.png", bbox_inches="tight")
        plt.show()

    def plot_survey_pairplots(self, ground_df):
        """
        Plots the pairplots.
        Args:
            ground_df (pd.DataFrame): Dataframe containing the data.
        """
        plt.figure(figsize=(12, 6))
        plt.suptitle("Pairplots", fontsize=16)
        selected = ground_df[self.numerical_columns + ["location_type"]]
        pairplot = sns.pairplot(selected, hue="location_type", kind="scatter", diag_kind="kde",
                                palette=set_color_palette(5))
        for i, j in zip(*plt.np.triu_indices_from(pairplot.axes, 1)):
            x_series = selected.iloc[:, j]
            y_series = selected.iloc[:, i]
            sns.regplot(x=x_series, y=y_series, ax=pairplot.axes[i, j], color="gray", scatter_kws={"alpha": 0.3})
        plt.tight_layout()
        plt.savefig(f"{self.path}_pairplots.png", bbox_inches="tight")
        plt.show()

    def plot_survey_data(self, ground_df):
        """
        Plots the survey data.
        Args:
            ground_df (pd.DataFrame): Dataframe containing the data.
        """
        self.plot_survey_boxplots(ground_df)
        self.plot_survey_histograms(ground_df)
        self.plot_survey_kde_plots(ground_df)
        self.plot_survey_heatmaps(ground_df)
        self.plot_survey_scatterplots(ground_df)
        self.plot_survey_countplots(ground_df)
        self.plot_survey_pairplots(ground_df)

    def plot_coldest_and_hottest_day(self, day_to_plot_hot, day_to_plot_cold, filtered_temperature_cold_df,
                                     filtered_temperature_hot_df):
        """
        Plots the data for the coldest and hottest day.
        Args:
            day_to_plot_hot (str): Day to plot the hottest day.
            day_to_plot_cold (str): Day to plot the coldest day.
            filtered_temperature_cold_df (pd.DataFrame): Dataframe containing the data for the coldest day.
            filtered_temperature_hot_df (pd.DataFrame): Dataframe containing the data for the hottest day.
        """
        day_to_plot_datetime_hot = pd.to_datetime(day_to_plot_hot)
        day_to_plot_datetime_cold = pd.to_datetime(day_to_plot_cold)
        fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(12, 6))
        fig.suptitle("Temperature Data for Coldest and Hottest Balconies")
        self.plot_temperature_data(axs[0, 0], filtered_temperature_cold_df, day_to_plot_datetime_cold,
                                   f"Coldest Balcony on Coldest Day ({day_to_plot_cold})")
        self.plot_temperature_data(axs[0, 1], filtered_temperature_cold_df, day_to_plot_datetime_hot,
                                   f"Coldest Balcony on Hottest Day ({day_to_plot_hot})")
        self.plot_temperature_data(axs[1, 0], filtered_temperature_hot_df, day_to_plot_datetime_cold,
                                   f"Hottest Balcony on Coldest Day ({day_to_plot_cold})")
        self.plot_temperature_data(axs[1, 1], filtered_temperature_hot_df, day_to_plot_datetime_hot,
                                   f"Hottest Balcony on Hottest Day ({day_to_plot_hot})")
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.savefig(f'{self.path}coldest_hottest_day_data_{pd.Timestamp.now().strftime("%Y-%m-%d")}.png',
                    bbox_inches="tight", )
        plt.show()

    def plot_max_hour_distribution(self, max_fyta_values_df, max_boum_values_df, name):
        """
        Plots the distribution of the maximum values.
        Args:
            max_fyta_values_df (pd.DataFrame): Dataframe containing the data.
            max_boum_values_df (pd.DataFrame): Dataframe containing the data.
            name (str): Name of the data.
        """
        today = pd.Timestamp(year=2023, month=10, day=30)
        max_fyta_values_df["max_light_time"] = max_fyta_values_df["max_light_time"].apply(
            lambda x: datetime.combine(today, x))
        max_fyta_values_df["max_temperature_time"] = max_fyta_values_df["max_temperature_time"].apply(
            lambda x: datetime.combine(today, x))
        max_boum_values_df["max_temperature_time_boum"] = max_boum_values_df["max_temperature_time_boum"].apply(
            lambda x: datetime.combine(today, x))
        max_boum_values_df["max_input_current_time_boum"] = max_boum_values_df["max_input_current_time_boum"].apply(
            lambda x: datetime.combine(today, x))
        max_fyta_values_df["max_light_hour"] = max_fyta_values_df["max_light_time"].dt.hour
        max_fyta_values_df["max_temperature_hour"] = max_fyta_values_df["max_temperature_time"].dt.hour
        max_boum_values_df["max_temperature_hour_boum"] = max_boum_values_df["max_temperature_time_boum"].dt.hour
        max_boum_values_df["max_input_current_hour"] = max_boum_values_df["max_input_current_time_boum"].dt.hour
        max_values_df = max_fyta_values_df[max_fyta_values_df["max_light_hour"] != 0]
        max_values_df = max_values_df[max_values_df["max_temperature_hour"] != 0]
        max_boum_values_df = max_boum_values_df[max_boum_values_df["max_temperature_hour_boum"] != 0]
        max_boum_values_df = max_boum_values_df[max_boum_values_df["max_input_current_hour"] != 0]
        sns.set(style="whitegrid")
        fig, axes = plt.subplots(3, 2, figsize=(24, 12))
        sns.histplot(data=max_values_df, x="max_light_hour", bins=24, kde=True, ax=axes[0, 0], hue="orientation")
        axes[0, 0].set_title(f"Distribution of Max Light Intensity Hours {name} Sensor")
        axes[0, 0].set_xlabel("Hour of the Day")
        axes[0, 0].set_xlim(0, 23)
        axes[0, 0].set_xticks(range(0, 24, 5))
        sns.histplot(data=max_values_df, x="max_temperature_hour", bins=24, kde=True, ax=axes[0, 1], hue="orientation")
        axes[0, 1].set_title(f"Distribution of Max Temperature Hours {name} Sensor")
        axes[0, 1].set_xlabel("Hour of the Day")
        axes[0, 1].set_xlim(0, 23)
        axes[0, 1].set_xticks(range(0, 24, 5))
        sns.histplot(data=max_boum_values_df, x="max_input_current_hour", bins=24, kde=True, ax=axes[2, 0],
                     hue="orientation")
        axes[1, 0].set_title("Distribution of Max Input Current Hours Boum Sensor")
        axes[1, 0].set_xlabel("Hour of the Day")
        axes[1, 0].set_xlim(0, 23)
        axes[1, 0].set_xticks(range(0, 24, 5))
        sns.histplot(data=max_boum_values_df, x="max_temperature_hour_boum", bins=24, kde=True, ax=axes[1, 1],
                     hue="orientation")
        axes[1, 1].set_title("Distribution of Max Temperature Hours Boum Sensor")
        axes[1, 1].set_xlabel("Hour of the Day")
        axes[1, 1].set_xlim(0, 23)
        axes[1, 1].set_xticks(range(0, 24, 5))
        fig.delaxes(axes[2, 1])
        plt.tight_layout()
        plt.savefig(f'{self.path}max_hour_distribution_{name}_{pd.Timestamp.now().strftime("%Y-%m-%d")}.jpeg',
                    bbox_inches="tight", dpi=900)
        plt.show()

    def plot_fyta_and_boum_data_comparison(self, df, days):
        """
        Plots the FYTA and Boum data comparison.
        Args:
            df (pd.DataFrame): Dataframe containing the data.
            days (int): Number of days to plot.
        """
        df_filtered = df[
            df.index - timedelta(days=1) > pd.Timestamp(year=2023, month=10, day=30) - timedelta(days=days)]
        fig, axes = plt.subplots(10, 2, figsize=(80, 40))
        color_palette = sns.color_palette("colorblind")
        line_styles = ["-", "--", "-.", ":"]
        for i, balcony in enumerate(self.sensor_dict.keys()):
            ax1 = axes[i, 0]
            ax2 = ax1.twinx()
            ax2.twinx()
            ax4 = axes[i, 1]
            boum_device = self.device_dict[balcony][:8]
            boum_temp_col = df_filtered["temperature_boum"][f"temperature_boum_{boum_device}"]
            boum_temp_col.plot(ax=ax1, label=f"Boum Temp ({boum_device})")
            for j, sensor in enumerate(self.sensor_dict[balcony]):
                fyta_temp_col = df_filtered["temperature"][f"temperature_{sensor}"]
                fyta_light_col = df_filtered["light"][f"light_{sensor}"]
                fyta_light_col.plot(ax=ax4, color=color_palette[j + 3],
                                    label=f"FYTA Light ({sensor}, {self.find_keys_by_value(sensor)})",
                                    linestyle=line_styles[j])
                fyta_temp_col.plot(ax=ax1, color=color_palette[j + 4],
                                   label=f"FYTA Temp ({sensor}, {self.find_keys_by_value(sensor)})",
                                   linestyle=line_styles[j])
            self.set_labels(ax1, balcony, "Temperature (°C)")
            self.set_labels(ax4, balcony, "Light")
            ax4.set_ylabel("Light Intensity")
            ax1.legend(loc="upper right", frameon=False)
            ax4.legend(loc="upper left", frameon=False)
            ax1.set_ylim(0, 71)
            ax4.set_ylim(0, 3501)
            ax1.set_yticks(range(0, 70, 10))
            ax4.set_yticks(range(0, 3500, 500))
            plt.tight_layout()
        plt.tight_layout()
        plt.savefig(f"{self.path}/fyta_and_boum_data_comparison.png")
        plt.show()
        return

    @staticmethod
    def set_labels(arg0, balcony, arg2):
        """
        Sets the labels for the plot.
        Args:
            arg0 (matplotlib.axes._subplots.AxesSubplot): Axes object.
            balcony (str): Balcony name
            arg2 (str): Y-axis label.
        """
        arg0.set_title(f"FYTA And Boum Data Comparison - Balcony {balcony}")
        arg0.set_xlabel("Timestamp")
        arg0.set_ylabel(arg2)

    def find_keys_by_value(self, target_value):
        """
        Finds the key for the given value.
        Args:
            target_value (int): Target value.
        Returns:
            str: Key.
            None: If no key is found.
        """
        target_value = int(target_value)
        for key in self.sensor_location:
            for value in self.sensor_location[key]:
                if value == target_value:
                    return key

    def plot_average_day(self, df, sensor_list=None, boum_id="13235f69"):
        """
        Plots the average day.
        Args:
            df (pd.DataFrame): Dataframe containing the data.
            sensor_list (list, optional): List of sensors to plot (default: None).
            boum_id (str, optional): Boum ID (default: "13235f69").
        """
        if sensor_list is None:
            sensor_list = ["14541", "21356", "14539"]
        df_1 = df.select_dtypes(include="number")
        hourly_df_1 = df_1.groupby(df_1.index.hour).mean()

        fig, ax1 = plt.subplots(figsize=(12, 6))
        ax1.plot(hourly_df_1.index, hourly_df_1["temperature_boum"][f"temperature_boum_{boum_id}"],
                 label="Temperature Boum", )
        for sensor in sensor_list:
            ax1.plot(hourly_df_1.index, hourly_df_1["temperature"][f"temperature_{sensor}"],
                     label=f"Temperature {sensor}")
        ax1.plot(hourly_df_1.index, hourly_df_1["temperatureEsp_boum"][f"temperatureEsp_boum_{boum_id}"],
                 label="temperatureEsp_boum")
        ax1.plot(hourly_df_1.index, hourly_df_1["batteryVoltage_boum"][f"batteryVoltage_boum_{boum_id}"],
                 label="batteryVoltage_boum")
        ax1.plot(hourly_df_1.index, hourly_df_1["solarVoltage_boum"][f"solarVoltage_boum_{boum_id}"],
                 label="solarVoltage_boum")
        ax1.plot(hourly_df_1.index, hourly_df_1["inputCurrent_boum"][f"inputCurrent_boum_{boum_id}"],
                 label="inputCurrent_boum")
        ax1.set_xlabel("Hour of the Day")
        ax1.set_ylabel("Temperature", color="tab:blue")
        ax1.tick_params(axis="y", labelcolor="tab:blue")
        ax1.legend(loc="upper left")
        ax2 = ax1.twinx()
        for sensor in sensor_list:
            ax2.plot(hourly_df_1.index, hourly_df_1["light"][f"light_{sensor}"], linestyle="--",
                     label=f"Light {sensor}")
        self.set_lable_axis(ax2, "Light Intensity", "tab:orange", "upper left")
        ax3 = ax1.twinx()
        ax3.spines["right"].set_position(("outward", 60))  # Move the third y-axis to the right
        ax3.plot(hourly_df_1.index, hourly_df_1["solarVoltage_boum"][f"solarVoltage_boum_{boum_id}"], linestyle=":",
                 label="Solar Voltage", color="tab:green")
        ax3.plot(hourly_df_1.index, hourly_df_1["batteryVoltage_boum"][f"batteryVoltage_boum_{boum_id}"], linestyle=":",
                 label="Battery Voltage", color="tab:purple")
        self.set_lable_axis(ax3, "Voltage", "tab:green", "upper right")
        ax1.legend(loc="upper left", bbox_to_anchor=(0.3, -0.1), ncol=2)
        plt.title(f"Average Values by Hour of the Day Balcony with ID {boum_id}")
        plt.xticks(range(24))
        plt.grid(True)
        plt.tight_layout()
        plt.savefig("average_day.png", bbox_inches="tight")
        plt.show()

    @staticmethod
    def set_lable_axis(arg0, arg1, color, loc):
        """
        Sets the labels for the plot.
        Args:
            arg0 (matplotlib.axes._subplots.AxesSubplot): Axes object.
            arg1 (str): Y-axis label
            color (str): Color of the label.
            loc (str): Location of the legend.
        """
        arg0.set_ylabel(arg1, color=color)
        arg0.tick_params(axis="y", labelcolor=color)
        arg0.legend(loc=loc, frameon=False)
