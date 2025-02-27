import os
from m4.configuration import update_folder_paths as ufp # type: ignore
from alpao_simulator.ground.osutils import load_data_path

fn = ufp.folders

CONFIGURATION_FILE = os.path.join(os.path.dirname(__file__), 'sysconfig', 'configuration.conf')
CONFIGURATION_ROOT_FOLDER = CONFIGURATION_FILE.replace('configuration.conf', '')
BASE_PATH = load_data_path(CONFIGURATION_FILE)
INFLUENCE_FUNCTIONS_FOLDER = os.path.join(BASE_PATH, 'influence_functions')
if not os.path.exists(INFLUENCE_FUNCTIONS_FOLDER):
    os.makedirs(INFLUENCE_FUNCTIONS_FOLDER)
INTERF_CONF_FILE = os.path.join(CONFIGURATION_ROOT_FOLDER, 'InterfSettings.conf')
OPD_IMAGES_FOLDER = fn.OPD_IMAGES_ROOT_FOLDER

def INFLUENCE_FUNCTIONS_FILE(nacts):
    return os.path.join(INFLUENCE_FUNCTIONS_FOLDER, f'dm{nacts}_iffCube.fits')

def INTMAT_FILE(nacts):
    return os.path.join(INFLUENCE_FUNCTIONS_FOLDER, f'dm{nacts}_intmat.fits')

def ZERNMAT_FILE(nacts):
    return os.path.join(INFLUENCE_FUNCTIONS_FOLDER, f'dm{nacts}_zmat.fits')

def RECMAT_FILE(nacts):
    return os.path.join(INFLUENCE_FUNCTIONS_FOLDER, f'dm{nacts}_rmat.fits')
