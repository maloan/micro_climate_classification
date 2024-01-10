"""
msc/visualizing_overheating.py
This file contains functions for visualizing the overheating data.
"""
from datetime import timedelta

import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from pandas import read_pickle


def plot_overheating(data: pd.DataFrame):
    """
    Plots the overheating data.

    Args:
        data (pd.DataFrame): The data frame containing the overheating data.

    Returns:
        None
    """
    sns.set_style('whitegrid')
    sns.set_context('notebook')
    sns.set_palette("colorblind", 25)
    color_palette = sns.color_palette("colorblind", 25)
    voltage_threshold = 5.0
    window_size = timedelta(minutes=400)
    colors = color_palette
    plots_to_show = 2

    def extract_internal_external_temperatures():
        """
        Extracts the internal and external temperature columns.

        Returns:
            tuple: A tuple containing the internal temperature columns
            and the external temperature columns.
        """
        internal_temp_columns = ['temperature_boum_a2146308', 'temperature_boum_cc1b8cb9',
                                 'temperature_boum_655c77c8', 'temperature_boum_2a650b37',
                                 'temperature_boum_13235f69', 'temperature_boum_188be60e']
        external_temp_columns = [['temperature_21335', 'temperature_21334', 'temperature_21332'],
                                 ['temperature_21344', 'temperature_21346', 'temperature_21345'],
                                 ['temperature_21328', 'temperature_21331', 'temperature_21329'],
                                 ['temperature_21349', 'temperature_21351', 'temperature_21350'],
                                 ['temperature_21336', 'temperature_21338', 'temperature_21337']]
        return internal_temp_columns, external_temp_columns

    internal_temp_cols, external_temp_cols = extract_internal_external_temperatures()
    df_n = data.droplevel(0, axis=1)
    df_1_temp_voltage = df_n[internal_temp_cols].copy()
    fig, axs = plt.subplots(1, 2, figsize=(15, 6))
    axs = axs.flatten()
    subplot_counter = 0
    for internal_temp, external_temp in zip(
            internal_temp_cols[-plots_to_show:], external_temp_cols[-plots_to_show:]):
        # Plot the overheating data
        name = internal_temp[-8:]
        sol_col_name = f"solarVoltage_boum_{name}"
        first_occurrence_index = (df_n[sol_col_name] >= voltage_threshold).idxmax()
        ax1 = axs[subplot_counter]
        start_time = max(df_1_temp_voltage.index[0], first_occurrence_index - window_size)
        end_time = min(df_1_temp_voltage.index[-1], first_occurrence_index + window_size)
        filtered_df_temp_voltage = df_1_temp_voltage[
            (df_1_temp_voltage.index >= start_time) & (df_1_temp_voltage.index <= end_time)]
        filtered_df_solar_voltage = df_n[(df_n.index >= start_time) & (df_n.index <= end_time)]
        filtered_external_temp = df_n[external_temp][(df_n.index >= start_time) &
                                                     (df_n.index <= end_time)]
        ax1.plot(filtered_df_temp_voltage.index,
                 filtered_df_temp_voltage[internal_temp],
                 label="Internal Temperature",
                 color=colors[0])
        ax1.plot(filtered_external_temp.T.mean().index,
                 filtered_external_temp.T.mean(),
                 label="External Temperature",
                 color=colors[1])
        ax1.legend(loc='upper left')
        ax1.set_ylabel("Temperature [°C]")
        ax1.set_xlabel("Timestamp")
        ax1.set_ylim(15, 65)
        ax2 = ax1.twinx()
        ax2.plot(filtered_df_solar_voltage.index,
                 filtered_df_solar_voltage[sol_col_name],
                 label="Solar Voltage",
                 color=colors[2])
        ax2.fill_between(filtered_df_solar_voltage.index, 0,
                         filtered_df_solar_voltage[sol_col_name],
                         where=(filtered_df_solar_voltage[sol_col_name] >= voltage_threshold),
                         color='grey', alpha=0.3)
        ax2.set_ylim(1.5, 6.5)
        ax2.legend(loc='upper right')
        ax2.set_ylabel("Solar Voltage [V]")
        ax1.set_title(f"Zoomed-in Temperature and Solar Voltage (Sensor {subplot_counter})")

        subplot_counter += 1
    plt.tight_layout()
    plt.savefig("../plots/overheating_voltage.png")
    plt.show()


if __name__ == '__main__':
    df = read_pickle('../data/data_pickled')
    plot_overheating(df)

# %%
