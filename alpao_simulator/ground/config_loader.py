from configparser import ConfigParser
import alpao_simulator.folder_paths as fp


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
    _dmReader = ConfigParser()
    _dmReader.read(fp.CONFIGURATION_FILE)
    section_name = f'DM{Nacts}'
    if section_name in _dmReader:
        return _dmReader[section_name]
    else:
        raise ValueError(f"No configuration found for {Nacts} actuators")

def load_interf_configuration(name:str):
    """
    Loads the interferometer configuration.
    
    Parameters
    ----------
    name : str
        Name of the interferometer.
    
    Returns
    -------
    dict
        Dictionary containing the interferometer configuration.
    """
    _interfReader = ConfigParser()
    _interfReader.read(fp.INTERF_CONF_FILE)
    if name in _interfReader:
        return _interfReader[name]
    else:
        raise ValueError(f"No configuration found for {name} interferometer")