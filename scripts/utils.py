import globals as GLOBALS
from datetime import datetime, timedelta
from scipy.ndimage import zoom
import OpenVisus as ov
import numpy as np
import os
import json


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


def get_km_of_config(config):
    x_min = config["coordinates"]["x_min"]
    x_max = config["coordinates"]["x_max"]
    difference = x_max - x_min
    return int(difference * 4)


def resize_array(data):
    target_size = (250, 250)
    n = data.shape[0]
    zoom_factor = target_size[0] / n
    return zoom(data, (zoom_factor, zoom_factor), order=1)


def get_min_max_local(data, variable):
    min_values = []
    max_values = []

    for matrix in data:
        plane_values = matrix.copy()
        plane_values = plane_values[~np.isnan(plane_values)]

        if len(plane_values) != 0:
            min_values.append(float(np.percentile(plane_values, 2.5)))
            max_values.append(float(np.percentile(plane_values, 97.5)))
        else:
            min_values.append(min_values[-1])
            max_values.append(max_values[-1])

    return min_values, max_values


def get_min_max_per_month(dir, prefix):
    min_values = []
    max_values = []

    counter = 0
    while counter <= 89:
        file_path = dir + "/" + prefix + f"{counter}.bin"
        print("Reading file: ", file_path)
        data = np.fromfile(file_path, dtype=np.float16)
        data = data[~np.isnan(data)]
        if len(data) == 0:
            min_values.append(min_values[-1])
            max_values.append(max_values[-1])
        else:
            min_values.append(float(np.percentile(data, 2.5)))
            max_values.append(float(np.percentile(data, 97.5)))
        counter += 1
    return min_values, max_values


def get_min_max_vort():
    variable = "vorticity_uvw"
    directory = "/data"

    min_dict = {}
    max_dict = {}

    min_value = np.inf
    max_value = -np.inf

    start_time = datetime(2011, 9, 13, 0)
    end_time = datetime(2012, 11, 14, 0)
    actual_time = start_time

    year = int(start_time.year)
    month = int(start_time.month)

    while actual_time < end_time:
        prefix = f"{variable}_{year}_{month}_13_0_"

        min_values, max_values = get_min_max_per_month(directory, prefix)
        min_dict[f"{actual_time.date()}"] = min_values
        max_dict[f"{actual_time.date()}"] = max_values

        min_value = min(min_value, min(min_values))
        max_value = max(max_value, max(max_values))

        if month == 12:
            month = 1
            year += 1
        else:
            month += 1
        actual_time = datetime(year, month, 13, 0)

    write_min_max("VORT", min_value, max_value, min_dict, max_dict)


def load_json():
    filepath = "/metadata.json"
    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            try:
                data = json.load(file)  # Load existing JSON data
            except json.JSONDecodeError:
                data = {
                }  # Start with an empty dictionary if file is empty or invalid
    else:
        data = {}
    return data


def write_min_max(var, min_global, max_global, min_dict, max_dict):
    data = load_json()
    data[var] = {
        "min_global": min_global,
        "max_global": max_global,
        "min_local": min_dict,
        "max_local": max_dict,
    }
    with open(f"/metadata.json", "w") as file:
        json.dump(
            data,
            file,
            indent=4,
        )
