import os
import alpao_simulator.folder_paths as fp
from alpao_simulator.deformable_mirror import AlpaoDm

def main():
    dms = [97, 277, 468, 820]
    print(f"The following data will be stored in '{fp.INFLUENCE_FUNCTIONS_FOLDER}'.\n"\
          f"To change the folder, modify the 'path' in the '{fp.CONFIGURATION_FILE}' file.\n"
    )
    for Nacts in dms:
        if os.path.exists(fp.INFLUENCE_FUNCTIONS_FILE(Nacts)):
            print(f"DM {Nacts} simulation already exists.")
            response = input(f"Would you like to overwrite it? (y/n) ")
            if response == 'y':
                # Erase existing data
                os.remove(fp.INFLUENCE_FUNCTIONS_FILE(Nacts))
                os.remove(fp.INTMAT_FILE(Nacts))
                os.remove(fp.ZERNMAT_FILE(Nacts))
                os.remove(fp.RECMAT_FILE(Nacts))
            else:
                continue
        dm = AlpaoDm(Nacts)
        print("")

if __name__ == "__main__":
    main()
