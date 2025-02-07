import globals as GLOBALS

from datetime import datetime, timedelta
from scipy.ndimage import zoom
from pathlib import Path

import numpy as np
import OpenVisus as ov


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


def download_whole_cube(db, actual_time, variable):
    print(f"Start downloading {variable} data for: ", actual_time)
    start_counter = datetime.now()
    time_step = get_timestamp(actual_time)
    data3D = db.read(time=time_step, x=GLOBALS.X_RANGE, y=GLOBALS.Y_RANGE)
    print("Download finished - time needed: ", datetime.now() - start_counter)

    # Resize and filter data
    data3D_resized = np.array([resize_array(matrix) for matrix in data3D])
    data3D_resized = np.array(
        [filter_to_nan(matrix) for matrix in data3D_resized])

    # Flat each matrix to row
    data3D_flat = np.array(
        [matrix.reshape(1, 250 * 250) for matrix in data3D_resized])

    # Use float16 to save space
    data_array_16 = np.array(data3D_flat, dtype=np.float16)

    # Save each layer separately
    for i, data in enumerate(data_array_16):
        filename = Path(f"/data/" + variable + "_" + str(actual_time.year) +
                        "_" + str(actual_time.month) + "_" +
                        str(actual_time.day) + "_" + str(actual_time.hour) +
                        "_" + str(i) + ".csv")
        np.savetxt(filename, data, delimiter=",", fmt='%f')
    print("Data saved successfully")


def start_download_whole_cube(variable):
    script_start = datetime.now()

    db = get_db(variable)
    start_time = datetime(2011, 9, 13, 0)
    end_time = datetime(2012, 11, 14, 0)
    actual_time = start_time

    year = int(start_time.year)
    month = int(start_time.month)

    while actual_time < end_time:
        download_whole_cube(db, actual_time, variable)
        if month == 12:
            month = 1
            year += 1
        else:
            month += 1
        actual_time = datetime(year, month, 13, 0)

    print("Script finished in: ", datetime.now() - script_start)
