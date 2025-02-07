import globals as GLOBALS
from datetime import datetime, timedelta
from scipy.ndimage import zoom
import OpenVisus as ov
import numpy as np


def get_db(variable):
    variable = GLOBALS.VAR_TO_LINK[variable]
    return ov.LoadDataset(variable)


def get_timestamp(target_datetime):
    start_datetime = datetime(2011, 9, 13, 0)
    total_timestamps = 10269
    time_difference = target_datetime - start_datetime

    if time_difference.total_seconds() >= 0:
        index = int(time_difference / timedelta(hours=1))
        if index < total_timestamps:
            return index
        else:
            print("Timestamp out of range: Later than {}".format(
                start_datetime + timedelta(hours=total_timestamps)))
    else:
        print("Timestamp out of range: Earlier than {}".format(start_datetime))


def filter_to_nan(data):
    data[data == 0] = np.nan
    return data


def resize_array(data):
    target_size = (250, 250)
    n = data.shape[0]
    zoom_factor = target_size[0] / n
    return zoom(data, (zoom_factor, zoom_factor), order=1)
