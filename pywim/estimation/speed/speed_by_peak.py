from pywim.utils.stats import iqr

import numpy as np
import pandas as pd
import peakutils


def sensors_estimation(
    signal_data: pd.DataFrame, sensors_delta_distance: list
) -> [np.array]:
    """

    :param signal_data:
    :param sensors_delta_distance:
    :return:
    """
    # x axis: time
    x = signal_data.index.values

    sensors_peak_time = []
    sensors_delta_time = [None]

    for k in signal_data.keys():
        # y axis: volts
        y = signal_data[k].values

        indexes = peakutils.indexes(y, thres=0.5, min_dist=30)

        sensors_peak_time.append(x[indexes])

    for i in range(1, len(sensors_peak_time)):
        sensors_delta_time.append(
            sensors_peak_time[i] - sensors_peak_time[i - 1]
        )

    # the information about first sensor should be equal to the second sensor
    sensors_delta_time[0] = sensors_delta_time[1]

    sensors_delta_speed = []

    for i in range(len(sensors_delta_distance)):
        sensors_delta_speed.append(
            sensors_delta_distance[i] / sensors_delta_time[i]
        )

    # the information about first sensor should be equal to the second sensor
    sensors_delta_speed[0] = sensors_delta_speed[1]

    return sensors_delta_speed


def average_estimation(
    signal_data: pd.DataFrame=None,
    sensors_delta_distance: list=None,
    sensors_delta_speed: list=None
) -> float:
    """

    :param signal_data:
    :param sensors_delta_distance:
    :param sensors_delta_speed:
    :return:
    """
    if not sensors_delta_speed:
        sensors_delta_speed = sensors_estimation(
            signal_data, sensors_delta_distance
        )

    speed_values = np.array([])

    for sensor_speeds in sensors_delta_speed[1:]:
        speed_values = np.concatenate((speed_values, sensor_speeds))

    return iqr.reject_outliers(pd.Series(speed_values)).mean()
