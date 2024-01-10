"""
This module contains functions for merging three dataframes based on their timestamps.
"""
import numpy as np
import pandas as pd

from API_and_Data.save_data import save_data


def merge_dataframe(data_1, data_2, data_3, norm=False):
    """
    Merges three dataframes based on their timestamps, normalizing the data if specified.

    Args:
        data_1 (DataFrame): The first dataframe to merge.
        data_2 (DataFrame): The second dataframe to merge.
        data_3 (DataFrame): The third dataframe to merge.
        norm (bool, optional): Whether to normalize the data (default: False).

    Returns:
        DataFrame: The merged and normalized dataframe.
    """
    for data in [data_1, data_2, data_3]:
        if "Unnamed: 0" in data.columns:
            data.drop(columns=["Unnamed: 0"], inplace=True)
    dataframe = pd.merge_ordered(pd.merge_ordered(
        data_1, data_2, on="timestamp"), data_3, on="timestamp")
    dataframe = dataframe.copy()
    dataframe["timestamp"] = pd.to_datetime(dataframe.timestamp).dt.tz_localize(None)
    dataframe["timestamp"] = dataframe["timestamp"].apply(lambda x: x.value // 10 ** 6 // 1000)
    dataframe["timestamp"] = pd.to_datetime(dataframe["timestamp"], unit="s")
    dataframe["time"] = dataframe["timestamp"]
    save_data("complete-dataframe", dataframe)
    dataframe = dataframe.set_index("timestamp")
    base_names = dataframe.columns.str.rsplit("_", n=1).str[0]
    columns = pd.MultiIndex.from_arrays([base_names, dataframe.columns])
    df_new = dataframe.copy()
    df_new.columns = columns
    dataframe = normalize_df(df_new) if norm else group_index(df_new)
    print("Done retrieving and saving weather_data.")
    return dataframe


def group_index(data):
    """
    Groups the dataframe by its index level and selects only numeric columns.

    Args:
        data (DataFrame): The dataframe to group.

    Returns:
        DataFrame: The grouped and numeric dataframe.
    """
    df_grouped = data.groupby(level=0, axis=1).apply(lambda x: x.select_dtypes(include=np.number))
    df_grouped.columns = df_grouped.columns.droplevel(0)
    dataframe = data.drop(columns=df_grouped.columns, axis=1)
    dataframe = pd.merge_ordered(dataframe, df_grouped, on="timestamp")
    dataframe = dataframe.copy()
    save_data("complete-dataframe", dataframe)
    dataframe.set_index("timestamp", inplace=True)
    return dataframe


def normalize_df(data):
    """
    Normalizes the dataframe by dividing each column by its maximum value.

    Args:
        data (DataFrame): The dataframe to normalize.

    Returns:
        DataFrame: The normalized dataframe.
    """
    df_norm = data.groupby(level=0, axis=1).apply(
        lambda x: x.select_dtypes(include=np.number) / x.select_dtypes(include=np.number).max())
    df_norm.columns = df_norm.columns.droplevel(0)
    dataframe = data.drop(columns=df_norm.columns, axis=1)
    dataframe = pd.merge_ordered(dataframe, df_norm, on="timestamp")
    save_data("norm-complete-dataframe", dataframe)
    dataframe.set_index("timestamp", inplace=True)
    return dataframe


if __name__ == "__main__":
    data1 = pd.read_csv("../data/fyta-dataframe.measurements.csv", low_memory=False)
    data2 = pd.read_csv("../data/boum-dataframe.measurements.csv")
    data3 = pd.read_csv("../data/weather-dataframe.measurements.csv")
    df_n = merge_dataframe(data1, data2, data3, True)  # For normalization
    df_x = merge_dataframe(data1, data2, data3, False)  # Without normalization
