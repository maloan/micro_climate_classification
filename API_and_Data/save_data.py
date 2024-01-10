"""
This is a script for checking if the last save was made today.
It saves the data to a CSV file if it was not saved today or more than 7 days ago.
"""
import glob
from datetime import datetime, date

import pandas as pd

current_date = datetime.now().date()


def check_last_save(last_save_date: datetime.date) -> bool:
    """
    This function checks
    if the time difference between the current date and the
    last save date is equal to zero or more than 7 days.

    Args:
        last_save_date (datetime.date): The last save date.

    Returns:
        bool: A boolean value indicating if the time difference
        is equal to zero or more than 7 days.
    """
    time_difference = current_date - last_save_date
    return time_difference.days == 0 or time_difference.days > 7


def find_last_save_date(name: str) -> (date, int):
    """
    This function finds the last date a file with the given name was saved.
    If no file with the given name exists, it returns the current date and 0.
    If a file with the given name exists,
    it returns the latest save date and the number of days since the last save.

    Args:
        name (str): The name of the file, including the file extension.

    Returns:
        (latest_save_date, time_difference) (date, int):
        A tuple containing the latest save date and the number of days since the last save.
    """
    curr_date = datetime.now().date()
    saved_files = glob.glob(f"../data/{name}.measurements_*.csv")
    if not saved_files:
        return curr_date, 0
    latest_file = max(saved_files)
    latest_save_date_str = latest_file.split("_")[1].split(".")[0]
    latest_save_date = datetime.strptime(latest_save_date_str, "%Y-%m-%d").date()
    time_difference = latest_save_date - curr_date
    time_difference = max(abs(time_difference.days), 0)
    return latest_save_date, time_difference


def save_data(name: str, data: pd.DataFrame):
    """
    Saves data as a CSV file in the data directory.

    Args:
        name (str): The name of the file, including the file extension.
        data (pd.DataFrame): A dataframe to be saved.

    Returns:
        None
    """
    dataframe = pd.DataFrame(data)
    df_new = dataframe.copy()
    df_new["save_date"] = current_date
    filename = f"../data/{name}.measurements_{current_date}.csv"
    df_new.to_csv(filename, index=False)
    print(f"Measurements saved successfully as {filename}.")


def create_file(name: str, data: pd.DataFrame):
    """
    Saves a list of data as a CSV file in the data directory.

    Args:
        name (str): The name of the file, including the file extension.
        data (pd.DataFrame): A list of data to be saved.

    Returns:
        None
    """
    dataframe = pd.DataFrame(data)
    df_new = dataframe.copy()
    df_new["save_date"] = current_date
    filename = f"../data/{name}.measurements_{current_date}.csv"
    df_new.to_csv(filename, index=False)
    print(f"Measurements saved successfully as {filename}.")


if __name__ == "__main__":
    save_data("test", pd.DataFrame([1, 2, 3]))
    create_file("test1", pd.DataFrame([1, 2, 3]))
    create_file("test2", pd.DataFrame([1, 2, 3]))
