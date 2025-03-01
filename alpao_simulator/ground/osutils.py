import time
from numpy import uint8
from astropy.io import fits
from numpy.ma import masked_array
from configparser import ConfigParser

def load_fits(filepath):
    """
    Loads a FITS file.
    
    Parameters
    ----------
    filepath : str
        Path to the FITS file.
    
    Returns
    -------
    np.array
        FITS file data.
    """
    with fits.open(filepath) as hdul:
        fit = hdul[0].data
        if len(hdul) > 1 and hasattr(hdul[1], 'data'):
            mask = hdul[1].data.astype(bool)
            fit = masked_array(fit, mask=mask)
    return fit

def save_fits(filepath, data):
    """
    Saves a FITS file.
    
    Parameters
    ----------
    filepath : str
        Path to the FITS file.
    
    data : np.array
        Data to be saved.
    """
    if isinstance(data, masked_array):
        fits.writeto(filepath, data.data, overwrite=True)
        if hasattr(data, 'mask'):
            fits.append(filepath, data.mask.astype(uint8))
    else:
        fits.writeto(filepath, data, overwrite=True)
        
def newtn():
    """
    Returns a timestamp in a string of the format `YYYYMMDD_HHMMSS`.
    
    Returns
    -------
    str
        Current time in a string format.
    """
    return time.strftime("%Y%m%d_%H%M%S")

def load_data_path(config_file):
    """
    Loads a data path from the configuration file.
    
    Parameters
    ----------
    config_file : str
        Path to the configuration file.
    key : str
        Key for the data path.
    
    Returns
    -------
    str
        Data path.
    """
    _dmReader = ConfigParser()
    _dmReader.read(config_file)
    return _dmReader['DATA']['path']
