import numpy as np
import pandas as pd


DAQmx_Val_GroupByChannel = 0


def gen_slope():
    f = lambda x: (-(x)**2 + 7)

    slope = [
        f(i) for i in np.linspace(-3, 3, 400)
    ]
    slope -= min(slope)

    return slope


def gen_synthetic_analog_data(
    sample_rate: int, total_seconds: float, time_delay: float, noise_p=200
):
    """

    :param sample_rate:
    :param total_seconds:
    :param time_delay:
    :param noise_p:
    :return:
    """
    total_points = total_seconds*sample_rate
    x = np.linspace(0, total_seconds, total_points)
    y = np.zeros(total_points)

    delay = int((time_delay/10) * sample_rate)
    axl = [delay + 200]

    for i in [delay] + axl:
        j = i*10
        y[j-200:j+200] = gen_slope()

    y += np.random.random(total_points)/noise_p  # noise
    y += np.random.randint(0, 100)/70  # changes baseline
    return pd.Series(y, index=x)


def gen_synthetic_digital_data(
    sample_rate: int, total_seconds: float, time_delay: float
):
    """

    :param sample_rate:
    :param total_seconds:
    :param time_delay:
    :return:

    """
    total_points = total_seconds*sample_rate
    x = np.linspace(0, total_seconds, total_points)
    y = np.zeros(total_points)

    delay = int((time_delay/10) * sample_rate)
    axles = [delay*10 - 1000, delay*10 + 3000]

    y[axles[0]:axles[1]] = 1
    y += np.random.random(total_points)/400.  # noise

    return pd.Series(y, index=x)


def int32():
    pass


def byref(arg):
    return arg


class Task:
    def CreateAIVoltageChan(self, **kargs):
        pass

    def CfgSampClkTiming(self, **kargs):
        pass

    def StartTask(self):
        pass

    def StopTask(self):
        pass

    def ClearTask(self):
        pass

    def ExportSignal(self, **kargs):
        pass

    def CfgDigEdgeStartTrig(self, **kargs):
        pass

    def ReadAnalogF64(self, *args, **kwargs):
        return gen_synthetic_analog_data(5000, 3.0, 1)

    def CreateDIChan(self, **kwargs):
        pass

    def CfgSampClkTiming(self, **kwargs):
        pass

    def ReadDigitalLines(self, *args, **kwargs):
        gen_synthetic_digital_data(5000, 3.0, 1)
