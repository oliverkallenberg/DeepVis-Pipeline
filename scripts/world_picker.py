import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import RectangleSelector
import yaml
import os

CONFIG = "/config.yml"


def update_config(file_path, x_min, x_max, y_min, y_max):
    #Loading existing config
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file) or {}
    else:
        data = {}

    # Update the coordinates with the global values
    if 'coordinates' not in data:
        data['coordinates'] = {}

    data['coordinates']['x_min'] = int(x_min)
    data['coordinates']['x_max'] = int(x_max)
    data['coordinates']['y_min'] = int(y_min)
    data['coordinates']['y_max'] = int(y_max)

    # Save the updated or default data back to the file
    with open(file_path, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)
        print(f"Configuration saved to {file_path}.")


def toggle_selector(event):
    if event.key in ['Q', 'q'] and toggle_selector.RS.active:
        print('RectangleSelector deactivated.')
        toggle_selector.RS.set_active(False)


def line_select_callback(eclick, erelease):
    'eclick and erelease are the press and release events'
    x1, y1 = eclick.xdata, eclick.ydata
    x2, y2 = erelease.xdata, erelease.ydata
    update_config(CONFIG, x_max=x1, x_min=x2, y_max=y1, y_min=y2)


def select_from_csv(csv_file_path):
    # Load data from CSV using numpy. Since it's a single line, we can use loadtxt.
    data_array = np.loadtxt(csv_file_path, delimiter=',')

    #reshoape Data
    resolution = int(np.sqrt(data_array.size))
    data_array = data_array.reshape((resolution, resolution))

    # Flip the data vertically to correct the orientation
    data_array = np.flipud(data_array)

    #Display with square picker
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.imshow(data_array, cmap='viridis')

    toggle_selector.RS = RectangleSelector(ax,
                                           line_select_callback,
                                           useblit=True,
                                           button=[1, 3],
                                           minspanx=5,
                                           minspany=5,
                                           spancoords='pixels',
                                           interactive=True)
    plt.connect('key_press_event', toggle_selector)
    plt.show()


# Example usage:
csv_file_path = r"D:\SVDaten\data\vorticity_uv_2011_9_13_0_0.csv"
resolution = 250  # Ensure this matches the dimensions you want to reshape your data into
select_from_csv(csv_file_path)
