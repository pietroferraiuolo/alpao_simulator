import numpy as np
from matplotlib import pyplot as plt
import alpao_simulator.ground.config_loader as cl

def getDmCoordinates(Nacts: int):
    """
    Generates the coordinates of the DM actuators for a given DM size and actuator sequence.
    
    Parameters
    ----------
    Nacts : int
        Total number of actuators in the DM.

    Returns
    -------
    np.array
        Array of coordinates of the actuators.
    """
    dms = cl.load_dm_configuration(Nacts)
    nacts_row_sequence = eval(dms['coords'])
    n_dim = nacts_row_sequence[-1]
    upper_rows = nacts_row_sequence[:-1]
    lower_rows = [l for l in reversed(upper_rows)]
    center_rows = [n_dim] * upper_rows[0]
    rows_number_of_acts = upper_rows + center_rows + lower_rows
    N_acts = sum(rows_number_of_acts)
    n_rows = len(rows_number_of_acts)
    cx = np.array([], dtype=int)
    cy = np.array([], dtype=int)
    for i in range(n_rows):
        cx = np.concatenate((cx, np.arange(rows_number_of_acts[i]) + (n_dim - rows_number_of_acts[i]) // 2))
        cy = np.concatenate((cy, np.full(rows_number_of_acts[i], i)))
    coords = np.array([cx, cy])
    return coords

def createMask(nActs: int, shape=(512, 512)):
    """
    Generates a circular mask for a mirror based on its optical diameter and pixel scale.
    
    Parameters
    ----------
    opt_diameter : float
        The mirror's diameter in millimeters.
    pixel_scale : float
        Scale in pixels per millimeter.
    shape : tuple, optional
        The shape of the output mask (height, width), by default (512, 512).
    
    Returns
    -------
    np.ndarray
        A boolean array of the given shape. True values represent the mirror area.
    """
    dm = cl.load_dm_configuration(nActs)
    opt_diameter = float(dm['opt_diameter'])
    pixel_scale = float(dm['pixel_scale'])
    height, width = shape
    cx, cy = width / 2, height / 2
    radius = (opt_diameter * pixel_scale) / 2  # radius in pixels
    y, x = np.ogrid[:height, :width]
    mask = (x - cx) ** 2 + (y - cy) ** 2 >= radius ** 2
    return mask

def pixel_scale(nacts:int):
    """
    Returns the pixel scale of the DM.
    
    Parameters
    ----------
    nacts : int
        Number of actuators in the DM.
    
    Returns
    -------
    float
        Pixel scale of the DM.
    """
    dm = cl.load_dm_configuration(nacts)
    return float(dm['pixel_scale'])

def plotDmCoordinates(Nacts: int, amplitude=None):
    """
    Plots the DM actuator coordinates for a given DM size.
    
    Parameters
    ----------
    Nacts : int
        Number of actuators in the DM.
    
    amplitude : float
        Amplitude of each actuator. If provided, the actuators will be color-coded
        based on their amplitude.
    """
    coords = getDmCoordinates(Nacts)
    plt.figure(figsize=(10, 8))
    if amplitude is None:
        plt.scatter(coords[0], coords[1], c='firebrick', s=100)
        plt.scatter(coords[0], coords[1], c='white', s=8)
        plt.scatter(coords[0], coords[1], c='b', s=2)
    else:
        plt.scatter(coords[0], coords[1], c=amplitude, cmap='rainbow', s=100)
    plt.gca().invert_yaxis()
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(f'ALPAO DM {Nacts} Actuator Coordinates')
    plt.colorbar()
    plt.show()