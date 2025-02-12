import argparse
from alpao_simulator import deformable_mirror as _dm
from alpao_simulator import interferometer as _interf

def main():
    parser = argparse.ArgumentParser(description="Initialize Alpao Simulator with a specified number of actuators.")
    parser.add_argument("--actuators", type=int, default=97,
                        help="Number of actuators for the deformable mirror (default: 97)")
    args = parser.parse_args()

    print("\nAlpao Simulator initialized.\n")
    dm = _dm.AlpaoDm(args.actuators)
    interf = _interf.Interferometer(dm)
    print(f"Interferometer initialized: {interf.model}\n")

if __name__ == "__main__":
    main()