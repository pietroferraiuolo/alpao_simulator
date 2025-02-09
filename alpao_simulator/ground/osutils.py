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
    hdul = fits.HDUList()
    hdul.append(fits.PrimaryHDU(data=data))
    hdul.writeto(filepath, overwrite=True)
    if hasattr(data, 'mask'):
        hdul.append(fits.ImageHDU(data=data.mask.astype(int)))
        hdul.writeto(filepath, overwrite=True)

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
