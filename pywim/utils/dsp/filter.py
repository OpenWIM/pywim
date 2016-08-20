"""

"""
import numpy as np
from scipy import signal


def moving_average(a, n=6):
    """
    Filter moving average

    @param a: array
    @type a: numpy.array
    @return: array with filter
    @rtype: numpy.array

    """
    ret = np.cumsum(a, dtype=float)
    return (ret[n - 1:] - ret[:1 - n]) / n


def filtfilt(data: np.ndarray, order: int=1, lower_cut: float=0.12):
    """
    Apply filt filt scypy filter
    
    :param lower_cut: default 600Mz/5000fs = 0.12
    :param data: Signal data
    :type data: ndarray
    :param order: Order lowpass buttterworth
    :type order: int
    :return: Signal data filtered
    :rtype: np.ndarray
    
    """
    # Create an order lowpass butterworth filter.
    b, a = signal.butter(order, lower_cut)
    
    # Use filtfilt to apply the filter.
    return signal.filtfilt(b, a, data)
