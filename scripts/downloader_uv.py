import globals as GLOBALS
import utils

from datetime import datetime
from pathlib import Path

import numpy as np


def save_cube(array, actual_time):
    # Save each layer separately
    for i, data in enumerate(array):
        filename = Path("/data/uv_" + str(actual_time.year) + "_" +
                        str(actual_time.month) + "_" + str(actual_time.day) +
                        "_" + str(actual_time.hour) + "_" + str(i) + ".csv")
        np.savetxt(filename, data, delimiter=",", fmt='%f')
    print("Data saved successfully")


def transform_to_uv(array_u, array_v):
    uv_transformed = []
    for i in range(90):
        u_layer = array_u[i].reshape(1, 250 * 250)
        v_layer = array_v[i].reshape(1, 250 * 250)
        uv_layer = np.column_stack(
            (u_layer.ravel(), v_layer.ravel())).ravel().reshape(1, -1)
        uv_transformed.append(uv_layer)
    return np.array(uv_transformed, dtype=np.float16)


def download_whole_cube(db, actual_time, variable):
    print(f"Start downloading data {variable} for LIC textures: ", actual_time)
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
    return data_array_16


def start_download_uv():
    db_u = utils.get_db("u")
    db_v = utils.get_db("v")
    start_time = datetime(2011, 9, 13, 0)
    end_time = datetime(2012, 11, 14, 0)
    actual_time = start_time

    year = int(start_time.year)
    month = int(start_time.month)

    while actual_time < end_time:
        u_data = download_whole_cube(db_u, actual_time, "u")
        v_data = download_whole_cube(db_v, actual_time, "v")
        uv_data = transform_to_uv(u_data, v_data)
        save_cube(uv_data, actual_time)

        if month == 12:
            month = 1
            year += 1
        else:
            month += 1
        actual_time = datetime(year, month, 13, 0)
