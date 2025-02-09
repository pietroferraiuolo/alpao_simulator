import os
from alpao_simulator.ground.osutils import load_data_path

CONFIGURATION_FILE = os.path.join(os.path.dirname(__file__), 'sysconfig', 'configuration.ini')
BASE_PATH = load_data_path(CONFIGURATION_FILE)
DATA_ROOT_FOLDER = os.path.join(BASE_PATH, 'data')
CONFIGURATION_ROOT_FOLDER = os.path.join(BASE_PATH, 'sysconfig')
INFLUENCE_FUNCTIONS_FOLDER = os.path.join(DATA_ROOT_FOLDER, 'influence_functions')

def INFLUENCE_FUNCTIONS_FILE(nacts):
    return os.path.join(INFLUENCE_FUNCTIONS_FOLDER, f'dm{nacts}_iffCube.fits')

def INTMAT_FILE(nacts):
    return os.path.join(INFLUENCE_FUNCTIONS_FOLDER, f'dm{nacts}_intmat.fits')

def ZERNMAT_FILE(nacts):
    return os.path.join(INFLUENCE_FUNCTIONS_FOLDER, f'dm{nacts}_zmat.fits')

def RECMAT_FILE(nacts):
    return os.path.join(INFLUENCE_FUNCTIONS_FOLDER, f'dm{nacts}_rmat.fits')
