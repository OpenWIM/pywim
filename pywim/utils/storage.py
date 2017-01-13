"""
"""
from datetime import datetime

import h5py
import numpy as np
import pandas as pd


def create_new_file(
    path: str,
    date_time: datetime=datetime.now(),
    collection_type: str='d',
    site_id: str='001', lane_id: str='01'
) -> h5py.File:
    """

    :param path:
    :param date_time:
    :param collection_type:
    :param site_id:
    :param lane_id:
    :return: h5py.File

    """
    f_id = 'wim_{}_{}_{}_{}'.format(
        collection_type, site_id, lane_id,
        date_time.strftime('%Y%M%d')
    )

    return h5py.File('/{}/{}.h5'.format(path, f_id), 'w')


def create_data_set(
    data_file: h5py.File,
    data: pd.DataFrame,
    date_time: datetime=datetime.now(),
    site_id: str='000',
    lane_id: str='00',
    temperature: float=None,
    license_plate: str=None,
    sensor_calibration_factory: list=None,
    distance_between_sensors: list=None,
    sensor_type: str=None,
    sensors_layout: str=None,
    **kwargs
) -> h5py.Dataset:
    """

    :param data_file:
    :param data:
    :param date_time: (e.g. 2017-49-04 00:49:36)
    :param site_id: (e.g. 001)
    :param lane_id: (e.g. 01)
    :param temperature: (e.g. 28.5)
    :param license_plate: (e.g. AAA9999)
    :param sensor_calibration_factory: (e.g. [0.98, 0.99, 0.75])
    :param distance_between_sensors: (e.g. [1.0, 1.5, 2.0])
    :param sensor_type: (e.g. quartz, polymer, ceramic, mixed)
    :param sensors_layout: (e.g. |/|\|<|>|=|)
    :param kwargs:
    :return:
    """

    dset_id = 'run_{}_{}_{}'.format(
        site_id, lane_id, date_time.strftime('%Y%M%d_%H%M%S')
    )

    dset = data_file.create_dataset(
        dset_id, shape=(data.shape[0],),
        dtype=np.dtype([
            (k, float) for k in ['index'] + list(data.keys())
        ])
    )

    dset['index'] = data.index

    for k in data.keys():
        dset[k] = data[k]

    dset.attrs['date_time'] = date_time.strftime('%Y-%M-%d %H:%M:%S')
    dset.attrs['site_id'] = site_id
    dset.attrs['lane_id'] = lane_id
    dset.attrs['temperature'] = temperature
    dset.attrs['license_plate'] = license_plate
    dset.attrs['sensor_calibration_factory'] = sensor_calibration_factory
    dset.attrs['distance_between_sensors'] = distance_between_sensors
    dset.attrs['sensor_type'] = sensor_type
    dset.attrs['sensors_layout'] = sensors_layout

    if kwargs:
        for k, v in kwargs.items():
            dset.attrs[k] = v

    return dset


def open_file(file_path: str):
    """

    :param file_path:
    :return:
    """
    return h5py.File(file_path, 'r')


def dataset_to_dataframe(dset: h5py.Dataset):
    """

    :param dset:
    :return:
    """
    return pd.DataFrame(dset[dset.dtype.names[1:]], index=dset['index'])
