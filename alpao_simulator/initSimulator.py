import os
import sys
import argparse
from alpao_simulator.ground.geometry import rms
from alpao_simulator import deformable_mirror as _dm
from alpao_simulator import interferometer as _interf
from IPython import get_ipython


if "--" in sys.argv:
    sys.argv = sys.argv[sys.argv.index("--") + 1:]

parser = argparse.ArgumentParser(description="Initialize Alpao Simulator with a specified number of actuators.")
parser.add_argument("--actuators", type=int, default=97,
                    help="Number of actuators for the deformable mirror (default: 97)")
args = parser.parse_args()
ipython = get_ipython()
if ipython is not None:
    ipython.run_line_magic(magic_name="matplotlib", line = "qt")
    
print("\n"+' '*6+"ALPAO SIMULATOR")
dm = _dm.AlpaoDm(args.actuators)
print("")
interf = _interf.Interferometer(dm)
print(f"{interf.model} Interferometer initialized")

def import_m4_utilities():
    """Imports useful M4 software utilities for calibration"""
    global ifp, Flattening, IFFCapturePreparation, rd, ifm, fn
    from m4.dmutils import iff_processing as ifp
    from m4.dmutils.flattening import Flattening
    from m4.dmutils.iff_acquisition_preparation import IFFCapturePreparation
    from m4.ground import read_data as rd
    from scripts.misc.IFFPackage import iff_module as ifm
    from m4.configuration import config_folder_names as fn
    icp = IFFCapturePreparation(dm)
    print("M4 utilities imported")
