import numpy as np
import os


def compute_vorticity_from_file(uv_data_path):
    # Read the CSV file
    data = np.loadtxt(uv_data_path, delimiter=',')
    u = data[0::2]
    v = data[1::2]

    # Extract grid resolution
    resolution = np.sqrt(u.size)
    nx, ny = int(resolution), int(resolution)

    # Reshape velocity components into 2D arrays
    U = u.reshape(ny, nx)
    V = v.reshape(ny, nx)

    # Create a regular grid
    x = np.linspace(0, 1, nx)  # Assuming a normalized grid
    y = np.linspace(0, 1, ny)
    X, Y = np.meshgrid(x, y)

    # Compute vorticity: ω = ∂v/∂x - ∂u/∂y
    dx = x[1] - x[0]
    dy = y[1] - y[0]
    dV_dx = np.gradient(V, axis=1) / dx
    dU_dy = np.gradient(U, axis=0) / dy
    vorticity = dV_dx - dU_dy

    return vorticity.flatten()


def calc_all_vorticity():
    path = "/data"

    for filename in os.listdir(path):
        uv_data = os.path.join(path, filename)
        vort_name = "vorticity_uv" + filename[2:]

        if os.path.isfile(uv_data) and "uv" in filename:
            vorticity_flattend = compute_vorticity_from_file(uv_data)
            np.savetxt(os.path.join(path, vort_name), [vorticity_flattend],
                       delimiter=",")
