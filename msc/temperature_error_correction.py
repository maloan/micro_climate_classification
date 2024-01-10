"""
msc/temperature_error_correction.py
This script contains functions to correct for temperature errors in the data.
"""
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from pandas import read_pickle
from scipy import stats


def extract_internal_external_temperatures():
    """
    This function extracts the internal and external temperature columns from the dataframe.

    Returns:
        internal_temp_cols (list): A list of internal temperature column names.
        external_temp_cols (list): A list of external temperature column names.
    """
    internal_temp_cols = ['temperature_boum_a2146308', 'temperature_boum_cc1b8cb9',
                          'temperature_boum_655c77c8',
                          'temperature_boum_2a650b37', 'temperature_boum_13235f69',
                          'temperature_boum_a27e798c',
                          'temperature_boum_188be60e', 'temperature_boum_5fe95b01']
    external_temp_cols = [['temperature_21335', 'temperature_21334', 'temperature_21332'],
                          ['temperature_21344', 'temperature_21346', 'temperature_21345'],
                          ['temperature_21328', 'temperature_21331', 'temperature_21329'],
                          ['temperature_21349', 'temperature_21351', 'temperature_21350'],
                          ['temperature_14541', 'temperature_14539', 'temperature_21356'],
                          ['temperature_21336', 'temperature_21338', 'temperature_21337'],
                          ['temperature_21355', 'temperature_21348', 'temperature_21347'],
                          ['temperature_21352', 'temperature_21354', 'temperature_21353']]
    return internal_temp_cols, external_temp_cols


def calculate_correction_slopes_and_intercepts(internal_temp_cols, external_temp_cols):
    """
    This function calculates the correction slopes and intercepts for each sensor.

    Args:
        internal_temp_cols (list): A list of internal temperature column names.
        external_temp_cols (list): A list of external temperature column names.

    Returns:
        slopes (list): A list of correction slope values.
        intercepts (list): A list of correction intercept values.
    """
    slopes = []
    intercepts = []

    for internal_temp_col, external_temp_col in zip(internal_temp_cols, external_temp_cols):
        internal_temp = df['temperature_boum'][internal_temp_col]
        external_temp = df['temperature'][external_temp_col].T.mean()
        slope, intercept, _, _, _ = stats.linregress(internal_temp, external_temp)
        slopes.append(slope)
        intercepts.append(intercept)
    return slopes, intercepts


def sensor_error_correction(dataframe):
    """
    This function applies the correction slopes and intercepts to
    the dataframe to correct for sensor errors.

    Args:
        dataframe (pandas.DataFrame): The dataframe containing the temperature data.

    Returns:
        corrected_temperatures (pandas.DataFrame): The dataframe with the corrected temperatures.
        mean_slope (float): The mean correction slope.
        mean_intercept (float): The mean correction intercept.
    """
    if 'temperature_boum' not in dataframe or 'temperature' not in dataframe:
        raise ValueError("Required temperature weather_data not found in DataFrame")
    internal_temperatures, external_temperatures = extract_internal_external_temperatures()
    slopes, intercepts = calculate_correction_slopes_and_intercepts(
        internal_temperatures, external_temperatures)
    corrected_temperatures = {}
    for i, internal_temp_col in enumerate(internal_temperatures):
        slope = slopes[i]
        intercept = intercepts[i]
        corrected_temp = slope * dataframe['temperature_boum'][internal_temp_col] + intercept
        corrected_temperatures[internal_temp_col] = corrected_temp
    corrected_temperatures = pd.DataFrame(corrected_temperatures)
    mean_slope = np.mean(slopes)
    mean_intercept = np.mean(intercepts)
    return corrected_temperatures, mean_slope, mean_intercept


def correct_temperature_with_avg_model(internal_temp, mean_slope, mean_intercept):
    """
    This function applies the average correction model to correct for sensor errors.

    Args:
        internal_temp (pandas.Series): The internal temperature series.
        mean_slope (float): The mean correction slope.
        mean_intercept (float): The mean correction intercept.

    Returns:
        corrected_temperatures (pandas.Series): The corrected temperature series.
    """
    return mean_slope * internal_temp + mean_intercept


def plot_correction(original_temperatures, corrected_temperatures, mean_slope, mean_intercept):
    """
    This function plots the original and corrected temperature data with
    the average correction line.

    Args:
        original_temperatures (pandas.DataFrame): The dataframe containing
        the original temperature data.
        corrected_temperatures (pandas.DataFrame): The dataframe containing
        the corrected temperature data.
        mean_slope (float): The mean correction slope.
        mean_intercept (float): The mean correction intercept.
    """
    temp_range = np.linspace(original_temperatures.min().min(),
                             original_temperatures.max().max(), 100)
    avg_correction_line = mean_slope * temp_range + mean_intercept
    plt.figure(figsize=(12, 6))
    for sensor_col in original_temperatures.columns:
        plt.scatter(original_temperatures[sensor_col],
                    corrected_temperatures[sensor_col], alpha=0.3, s=2)
    plt.plot(temp_range, avg_correction_line,
             color="red", linestyle="--", label="Avg. Correction Trend")
    plt.title("Sensor Temperature Correction")
    plt.xlabel("Original Temperature [°C]")
    plt.ylabel("Corrected Temperature [°C]")
    plt.legend(loc='upper left')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("../plots/corrected_temperature_plot.png")
    plt.show()


if __name__ == '__main__':
    # Load the data
    df = read_pickle('../data/data_pickled')
    # Only use weather_data from August onwards as it is the most complete
    df = df[df.index.month >= 8]

    # Apply the correction
    corrected_temperatures_df, avg_slope, avg_intercept = sensor_error_correction(df)

    # Plot the correction
    plot_correction(df['temperature_boum'][
                        ['temperature_boum_a2146308', 'temperature_boum_cc1b8cb9',
                         'temperature_boum_655c77c8', 'temperature_boum_2a650b37',
                         'temperature_boum_13235f69', 'temperature_boum_a27e798c',
                         'temperature_boum_188be60e', 'temperature_boum_5fe95b01']],
                    corrected_temperatures_df, avg_slope, avg_intercept)

# %%
