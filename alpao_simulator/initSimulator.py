from alpao_simulator import deformable_mirror as _dm
from alpao_simulator import interferometer as _interf
print("\nAlpao Simulator initialized.\n")
dm = _dm.AlpaoDm(97)
interf = _interf.Interferometer(dm)
print(f"Interferometer initialized: {interf.model}\n")