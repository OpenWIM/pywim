from matplotlib import pyplot as plt
import os
import sys
import pandas as pd

# local
root_path = os.path.abspath(os.path.dirname(os.path.dirname(
    os.path.dirname(__file__)
)))

sys.path.insert(0, root_path)
from pywim.lib.daq.generic import (
    gen_synthetic_analog_data, gen_synthetic_digital_data
)


def test():
    ts_analog = gen_synthetic_analog_data(5000, 3.0, 1)
    ts_analog.plot()
    ts_digital = gen_synthetic_digital_data(5000, 3.0, 1)
    ts_digital.plot()
    plt.show()

if __name__ == '__main__':
    test()
