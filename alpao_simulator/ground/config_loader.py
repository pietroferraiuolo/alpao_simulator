from configparser import ConfigParser
import alpao_simulator.folder_paths as fp

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
