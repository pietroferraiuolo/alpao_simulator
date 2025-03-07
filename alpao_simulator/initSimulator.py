import os
import sys
import argparse
from alpao_simulator.ground.geometry import rms
from alpao_simulator import deformable_mirror as _dm
from alpao_simulator import interferometer as _interf
from IPython import get_ipython

# "measured" iff tns for each AlpaoDm available.
tns = {
    '88': '20250221_161425',
    '97': '20250221_121828',
    '277': '20250221_122151',
    '468': '20250221_122720',
    '820': '20250221_123831',
}

def _createHadamardMat(nacts):
    """
    Create a Hadamard matrix of size 2^nacts x 2^nacts.
    """
    from scipy.linalg import hadamard
    import math
    numb = math.ceil(math.log(nacts, 2))
    hadm = hadamard(2**numb)
    cmdBase = hadm[1 : nacts + 1, 1 : nacts + 1]
    return cmdBase

# bash alias argument parser
if "--" in sys.argv:
    sys.argv = sys.argv[sys.argv.index("--") + 1:]
parser = argparse.ArgumentParser(description="Initialize Alpao Simulator with a specified number of actuators.")
parser.add_argument("--actuators", type=int, default=88,
                    help="Number of actuators for the deformable mirror (default: 88)")
args = parser.parse_args()

# qt backend for live interferometer view
ipython = get_ipython()
if ipython is not None:
    ipython.run_line_magic(magic_name="matplotlib", line = "qt")

# simulator initialization, DM and interferometer
print("\n"+' '*6+"ALPAO SIMULATOR")
dm = _dm.AlpaoDm(args.actuators)
print("")
interf = _interf.Interferometer(dm)
print(f"{interf.model} Interferometer initialized")
hmat = _createHadamardMat(dm.nActs)

def import_m4_utilities():
    """Imports useful M4 software utilities for calibration"""
    global ifp, Flattening, IFFCapturePreparation, rd, ifm, fn
    from m4.dmutils import iff_processing as ifp
    from m4.dmutils.flattening import Flattening
    from m4.dmutils.iff_acquisition_preparation import IFFCapturePreparation
    from m4.ground import read_data as rd
    from m4.dmutils import iff_module as ifm
    from m4.configuration import config_folder_names as fn
    icp = IFFCapturePreparation(dm)
    print("M4 utilities imported")