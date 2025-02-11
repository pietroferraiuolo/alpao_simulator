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

def rebinned(img, rebin:int=1, sample:bool=False):
    """
    Image rebinner

    Replacement of IDL's rebin() function for 2d arrays.
    Resizes a 2d array by averaging or repeating elements.
    New dimensions must be integral factors of original dimensions,
    otherwise a ValueError exception will be raised.

    Parameters
    ----------
    img : masked_array
        Image to rebin.
    rebin : int, optional
        Rebinning factor. The default is 2.
    sample : bool
        if True, when reducing the array side elements are set
        using a nearest-neighbor algorithm instead of averaging.
        This parameter has no effect when enlarging the array.
       
    Returns
    -------
    newImg : masked_array
        Rebinned image.

    Raises
    ------
    ValueError
        in the following cases:
         - new_shape is not a sequence of 2 values that can be converted to int
         - new dimensions are not an integral factor of original dimensions
    NotImplementedError
         - one dimension requires an upsampling while the other requires
           a downsampling

    Examples
    --------
    >>> a = np.array([[0, 1], [2, 3]])
    >>> b = rebin(a, (4, 6)) #upsize
    >>> b
    array([[0, 0, 0, 1, 1, 1],
           [0, 0, 0, 1, 1, 1],
           [2, 2, 2, 3, 3, 3],
           [2, 2, 2, 3, 3, 3]])
    >>> rebin(b, (2, 3)) #downsize
    array([[0. , 0.5, 1. ],
           [2. , 2.5, 3. ]])
    >>> rebin(b, (2, 3), sample=True) #downsize
    array([[0, 0, 1],
           [2, 2, 3]])
    """
    a = img
    shape = img.shape
    new_shape = (shape[0]//rebin, shape[1]//rebin)
    # unpack early to allow any 2-length type for new_shape
    m, n = map(int, new_shape)
    if a.shape == (m, n):
        return a
    M, N = a.shape
    if m <= M and n <= M:
        if (M // m != M / m) or (N // n != N / n):
            raise ValueError("Cannot downsample by non-integer factors")
    elif M <= m and M <= m:
        if (m // M != m / M) or (n // N != n / N):
            raise ValueError("Cannot upsample by non-integer factors")
    else:
        raise NotImplementedError(
            "Up- and down-sampling in different axes " "is not supported"
        )
    if sample:
        slices = [slice(0, old, float(old) / new) for old, new in zip(a.shape, (m, n))]
        idx = np.mgrid[slices].astype(int)
        return a[tuple(idx)]
    else:
        if m <= M and n <= N:
            return a.reshape((m, M // m, n, N // n)).mean(3).mean(1)
        elif m >= M and n >= M:
            return np.repeat(np.repeat(a, m / M, axis=0), n / N, axis=1)


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
