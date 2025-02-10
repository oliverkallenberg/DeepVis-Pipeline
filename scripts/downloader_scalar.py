import globals as GLOBALS
import utils

from datetime import datetime
from pathlib import Path

import numpy as np


def get_min_max_local(data):
    min_values = []
    max_values = []

    for matrix in data:
        plane_values = matrix.copy()
        plane_values = plane_values[~np.isnan(plane_values)]
        min_values.append(float(np.percentile(plane_values, 2.5)))
        max_values.append(float(np.percentile(plane_values, 97.5)))
        return min_values, max_values


def download_whole_cube(db, actual_time, variable):
    print(f"Start downloading {variable} data for: ", actual_time)
    start_counter = datetime.now()
    time_step = utils.get_timestamp(actual_time)
    data3D = db.read(time=time_step, x=GLOBALS.X_RANGE, y=GLOBALS.Y_RANGE)
    print("Download finished - time needed: ", datetime.now() - start_counter)

    # Resize and filter data
    data3D_resized = np.array([utils.resize_array(matrix) for matrix in data3D])
    data3D_resized = np.array(
        [utils.filter_to_nan(matrix) for matrix in data3D_resized])

    # Flat each matrix to row
    data3D_flat = np.array(
        [matrix.reshape(1, 250 * 250) for matrix in data3D_resized])

    # Use float16 to save space
    data_array_16 = np.array(data3D_flat, dtype=np.float16)

    # extract min and max values for each layer
    min_values_local, max_values_local = utils.get_min_max_local(data_array_16)

    # Save each layer separately
    for i, data in enumerate(data_array_16):
        filename = Path("/data/" + variable + "_" + str(actual_time.year) +
                        "_" + str(actual_time.month) + "_" +
                        str(actual_time.day) + "_" + str(actual_time.hour) +
                        "_" + str(i) + ".csv")
        np.savetxt(filename, data, delimiter=",", fmt='%f')
    print("Data saved successfully")

    return min_values_local, max_values_local


def start_download_whole_cube(variable):
    script_start = datetime.now()

    db = utils.get_db(variable)
    start_time = datetime(2011, 9, 13, 0)
    end_time = datetime(2012, 11, 14, 0)
    actual_time = start_time

    year = int(start_time.year)
    month = int(start_time.month)

    min_dict_local = {}
    max_dict_local = {}

    min_value = np.inf
    max_value = -np.inf

    while actual_time < end_time:

        min_local, max_local = download_whole_cube(db, actual_time, variable)
        min_dict_local[f"{actual_time.date()}"] = min_local
        max_dict_local[f"{actual_time.date()}"] = max_local

        min_value = min(min_value, min(min_local))
        max_value = max(max_value, max(max_local))

        if month == 12:
            month = 1
            year += 1
        else:
            month += 1
        actual_time = datetime(year, month, 13, 0)

    print("Script finished in: ", datetime.now() - script_start)
