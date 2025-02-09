import folder_paths as fp
from astropy.io import fits
from numpy.ma import masked_array
from configparser import ConfigParser

_dmReader = ConfigParser()
_dmReader.read(fp.CONFIGURATION_FILE)

def load_dm_configuration(Nacts: int):
    """
    Loads the DM configuration for a given number of actuators.
    
    Parameters
    ----------
    Nacts : int
        Total number of actuators in the DM.
    
    Returns
    -------
    dict
        Dictionary containing the DM configuration.
    """
    section_name = f'DM{Nacts}'
    if section_name in _dmReader:
        return _dmReader[section_name]
    else:
        raise ValueError(f"No configuration found for {Nacts} actuators")
    
def load_data_path(key: str):
    """
    Loads a data path from the configuration file.
    
    Parameters
    ----------
    key : str
        Key for the data path.
    
    Returns
    -------
    str
        Data path.
    """
    return _dmReader['DATA'][key]
    
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