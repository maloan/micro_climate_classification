import math

import numpy as np


class Math:
    """Math helper class.

    Contains implementations of various mathematical functions
    used inside the TRACKTICS pipeline.

    """
    EPS = 1e-09

    @staticmethod
    def get_distance(df, dx, dy, cumsum=True):
        dfs = df.shift(1).fillna(0)
        disps_sq = (df[dx] - dfs[dx]).pow(2) + (df[dy] - dfs[dy]).pow(2)
        disps = np.sqrt(disps_sq)
        if cumsum:
            return disps.cumsum()
        else:
            return disps

    @staticmethod
    def get_norm(df, field1, field2):
        norm_sq = df[field1].pow(2) + df[field2].pow(2)
        return np.sqrt(norm_sq)

    @staticmethod
    def get_ndim_norm(df, *args):
        norm_sq = df[args[0]].pow(2)
        for _, arg in enumerate(args[1:]):
            norm_sq += df[arg].pow(2)
        return np.sqrt(norm_sq)

    @staticmethod
    def round_partial(value, resolution):
        """Rounds value to resoltion
        """
        return round(value / float(resolution)) * resolution

    @staticmethod
    def get_row_nearest(df, index, value_to_find):
        """Gets the row in a dataframe which is nearest
        to value_to_find which is a float.
        """
        Min = df[index] <= value_to_find
        Max = df[index] >= value_to_find
        idx_Min = df.ix[Min, index].idxmax()
        idx_Max = df.ix[Max, index].idxmin()
        return df.ix[idx_Min:idx_Max]

    @staticmethod
    def get_cov(sde, sdn, sdne):
        return np.array([[sde, sdne], [sdne, sdn]])

    @staticmethod
    def eigsorted(cov):
        vals, vecs = np.linalg.eigh(cov)
        order = vals.argsort()[::-1]
        return vals[order], vecs[:, order]

    @staticmethod
    def pts_to_wgs84(pts):
        pts = np.concatenate((pts, np.array([pts[0]])))  # make it closed
        wkt = ", ".join(map(lambda pt: "{} {}".format(pt[0], pt[1]), pts))
        return wkt

    @staticmethod
    def get_yaw_deg(df):
        return df.attitude * 180 / math.pi


def interpolate_dataframe(df, index_column, new_index_values, columns_to_interpolate, interpolation_method="values"):
    """
    Method to interpolate all columns of a dataframe which are in components to the new index passed.

    Args:
        df (Pandas.DataFrame): Dataframe to work on
        index_column (str or None): Name of the index column.
        If None, the dataframe's index is expected to be set and
            used.
            This also determines whether the returned dataframe still has the index as seperate column.
        new_index_values (list/ndarray): new index.
        x-values to interpolate new y-values from.
        columns_to_interpolate (list(str)): Name of the columns to use.
        interpolation_method (Optional[str]): Pandas interpolation method to use.
        Defaults to values.
        For other
            possibble methods see the documentation of  Pandas.DataFrame.interpolate().

    Returns:
        (:obj: `pd.DataFrame`): Pandas Dataframe with new index and interpoalted values.
    """

    # new dataframe object with selected columns and index
    interpolated_df = df[columns_to_interpolate].copy()

    # acquire array of indices from the original dataframe
    if index_column is not None:
        # if index_column is specified, copy it from the old dataframe and set it as index to the interpolated
        # dataframe, while keeping it as a column
        old_index = df[index_column]
        interpolated_df[index_column] = old_index
        interpolated_df.set_index(index_column, inplace=True, drop=False)

    # get the union of old and new index
    joined_index = np.array(sorted(list(set(new_index_values) | set(old_index))))

    # before reindexing, identify duplicate indices which may sometimes
    # occur
    idx = np.unique(interpolated_df.index, return_index=True)[1]
    interpolated_df = interpolated_df.iloc[idx].reindex(joined_index)

    # call pandas interpolation with the specified method
    interpolated_df.interpolate(method=interpolation_method, inplace=True)
    # if we have nulls (can happen if new index starts before old index) then
    # use previous values
    interpolated_df.fillna(method='bfill', inplace=True)
    interpolated_df.fillna(method='ffill', inplace=True)

    # determine the subset of indices which were only part of the old index
    indices_to_drop = sorted(list(set(old_index) - set(new_index_values)))

    # drop the rows not needed any more
    interpolated_df.drop(indices_to_drop, inplace=True)
    if index_column is not None:
        # this prevents errors in the last or first values (see tests)
        interpolated_df[index_column] = interpolated_df.index.values

    return interpolated_df


def interpolate_dataframe_to_resolution(df, index_column, resolution, columns_to_interpolate,
                                        interpolation_method="values"):
    """
    Method to interpolate all columns of a dataframe which are in components to a time-interval specified by the
    resolution.
    Note that this resolution is always starting from second.0 and the interpolated dataframe thus has
    a new index starting from second.x*resolution

    Args:
        df (Pandas.DataFrame): Dataframe to work on
        index_column (str or None): Name of the index column.
        If None, the dataframe's index is expected to be set and
            used.
            This also determines whether the returned dataframe still has the index as seperate column.
        resolution (float): resolution to interpolate dataframe to.
        columns_to_interpolate (list(str)): Name of the columns to use.
        interpolation_method (Optional[str]): Pandas interpolation method to use.
        Defaults to values.
        For other
            possibble methods see the documentation of  Pandas.DataFrame.interpolate().

    Returns:
        Pandas.DataFrame: Dataframe with new index according to resolution and interpoalted values.
    """

    # get the old index as numpy array
    old_index = df[index_column].values

    # round the first value to resolution.
    starttime = Math.round_partial(old_index[0], resolution)
    # if rounded value is larger than actual value, substract one resolution
    # step to not loose information
    if starttime - Math.EPS > old_index[0]:
        starttime -= resolution

    # round the last value to resolution.
    endtime = Math.round_partial(old_index[-1], resolution)
    # if rounded value is smaller than actual value, add one resolution step
    # to not loose information
    if endtime + Math.EPS < old_index[-1]:
        endtime += resolution

    # np.arange is unreliable with respect to including the endtime, so adding resolution
    # if resolution is very small, it can still fail to be included because of rounding errors
    # but we are OK with this loss of information
    new_index = np.arange(starttime, endtime + resolution, resolution)

    # given the new index, the interpolate dataframe function may be used.
    return interpolate_dataframe(df, index_column, new_index, columns_to_interpolate, interpolation_method)


def get_volume_boum_too(d):  # d = water table range in cm, measurement
    """Volume for a truncated cone
    """
    alpha = 8.13  # slope of the tank, assuming 40 cm diameter at top, and 30 cm diameter at bottom
    d = d / 100  # convert from cm to m
    H = 0.35  # in cm, depth of the tank is 30 cm
    r = 0.15  # in cm, inner radius at bottom of tank is 15 cm
    h = H - d
    R = h * np.tan(np.deg2rad(alpha)) + r  # R is the inner radius at the water table
    V = 1 / 3 * np.pi * h * (r ** 2 + r * R + R ** 2)
    return V * 1e3  # convert m3 to liter


def get_volume_boum_one(d):  # d = water table range in cm, measurement
    """Volume for a rectangular box
    """
    d = d / 100  # convert to m
    w = 0.365  # width in m
    t = 0.265  # depth (tiefe) in m
    H = 0.37  # height in m
    h = H - d
    V = w * t * h
    return V * 1e3  # convert m3 to liter
