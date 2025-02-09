import os
import config_loader as cl

BASE_PATH = cl.load_data_path('path')
DATA_ROOT_FOLDER = os.path.join(BASE_PATH, 'data')
CONFIGURATION_ROOT_FOLDER = os.path.join(BASE_PATH, 'data', 'sysconfig')
CONFIGURATION_FILE = os.path.join(CONFIGURATION_ROOT_FOLDER, 'configuration.ini')
INFLUENCE_FUNCTIONS_FOLDER = os.path.join(DATA_ROOT_FOLDER, 'influence_functions')

def INFLUENCE_FUNCTIONS_FILE(nacts):
    return os.path.join(INFLUENCE_FUNCTIONS_FOLDER, f'dm{nacts}_iffCube.fits')

def INTMAT_FILE(nacts):
    return os.path.join(INFLUENCE_FUNCTIONS_FOLDER, f'dm{nacts}_intmat.fits')

def ZERNMAT_FILE(nacts):
    return os.path.join(INFLUENCE_FUNCTIONS_FOLDER, f'dm{nacts}_zmat.fits')

def RECMAT_FILE(nacts):
    return os.path.join(INFLUENCE_FUNCTIONS_FOLDER, f'dm{nacts}_rmat.fits')
