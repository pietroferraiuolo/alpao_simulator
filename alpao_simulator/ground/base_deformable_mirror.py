import os
import numpy as np
from tps import ThinPlateSpline
from abc import ABC, abstractmethod
import alpao_simulator.ground.zernike as zern
import alpao_simulator.folder_paths as fp
import alpao_simulator.ground.osutils as osu
import alpao_simulator.ground.geometry as geometry


class BaseDeformableMirror(ABC):
    """
    Base class for deformable mirrors.
    """
    def __init__(self, nActs: int):
        """
        Initializes the base deformable mirror with the number of actuators.
        """
        self.mirrorModes = None
        self.nActs = nActs
        self._pxScale = geometry.pixel_scale(self.nActs)
        self.actCoords = geometry.getDmCoordinates(self.nActs)
        self.mask = geometry.createMask(self.nActs)
        self._scaledActCoords = self._scaleActCoords()
        self._iffCube = None
        self.IM = None
        self.ZM = None
        self.RM = None

        print(" "*11+f"DM {self.nActs}\n")
        self._load_matrices()


    @abstractmethod
    def set_shape(self, command: np.array, differential: bool = False):
        """
        Applies the DM to a wavefront.
        
        Parameters
        ----------
        command : np.array
            Wavefront to which the DM will be applied.

        differential : bool
            If True, the command is the differential wavefront.

        Returns
        -------
        np.array
            Modified wavefront.
        """
        raise NotImplementedError
    

    @abstractmethod
    def get_shape(self):
        """
        Returns the current shape of the DM.
        
        Returns
        -------
        np.array
            Current shape of the DM.
        """
        raise NotImplementedError
    

    def _load_matrices(self):
        """
        Loads the required matrices for the deformable mirror's operations.
        """
        if not os.path.exists(fp.INFLUENCE_FUNCTIONS_FILE(self.nActs)):
            print(f"First time simulating DM {self.nActs}. Generating influence functions...")
            self._simulate_Zonal_Iff_Acquisition()
        else:
            print(f"Loaded influence functions.")
            self._iffCube = np.ma.masked_array(osu.load_fits(fp.INFLUENCE_FUNCTIONS_FILE(self.nActs)))
        self._create_int_and_rec_matrices()
        self._create_zernike_matrix()

    
    def _create_zernike_matrix(self):
        """
        Create the Zernike matrix for the DM.
        """
        if not os.path.exists(fp.ZERNMAT_FILE(self.nActs)):
            n_zern = self.nActs
            print("Computing Zernike matrix...")
            self.ZM = zern.generate_zernike_matrix(n_zern, self.mask)
            osu.save_fits(fp.ZERNMAT_FILE(self.nActs), self.ZM)
        else:
            print(f"Loaded Zernike matrix.")
            self.ZM = osu.load_fits(fp.ZERNMAT_FILE(self.nActs))


    def _create_int_and_rec_matrices(self):
        """
        Create the interaction matrices for the DM.
        """
        if not os.path.exists(fp.INTMAT_FILE(self.nActs)):
            print("Computing interaction matrix...")
            self.IM = np.array(
                [
                    (self._iffCube[:, :, i].data)[self.mask == 0]
                    for i in range(self._iffCube.shape[2])
                ]
            )
            osu.save_fits(fp.INTMAT_FILE(self.nActs), self.IM)
        else:
            print(f"Loaded interaction matrix.")
            self.IM = osu.load_fits(fp.INTMAT_FILE(self.nActs))
        if not os.path.exists(fp.RECMAT_FILE(self.nActs)):
            print("Computing reconstruction matrix...")
            self.RM = np.linalg.pinv(self.IM)
            osu.save_fits(fp.RECMAT_FILE(self.nActs), self.RM)
        else:
            print(f"Loaded reconstruction matrix.")
            self.RM = osu.load_fits(fp.RECMAT_FILE(self.nActs))



    def _simulate_Zonal_Iff_Acquisition(self):
        """
        Simulate the influence functions by imposing 'perfect' zonal commands.
        
        Parameters
        ----------
        amps : float or np.ndarray, optional
            Amplitude(s) for the actuator commands. If a single float is provided,
            it is applied to all actuators. Default is 1.0.
            
        Returns
        -------
        np.ma.MaskedArray
            A masked cube of influence functions with shape (height, width, nActs).
        """
        # Get the number of actuators from the coordinates array.
        n_acts = self.actCoords.shape[1]
        max_x, max_y = self.mask.shape
        # Create pixel grid coordinates.
        pix_coords = np.zeros((max_x * max_y, 2))
        pix_coords[:, 0] = np.repeat(np.arange(max_x), max_y)
        pix_coords[:, 1] = np.tile(np.arange(max_y), max_x)
        # Convert actuator coordinates to pixel coordinates.
        # Note: self.coords is of shape (2, nActs) where first row is x and second is y.
        act_coords = self.actCoords.T  # shape: (n_acts, 2)
        act_pix_coords = np.zeros((n_acts, 2), dtype=int)
        act_pix_coords[:, 0] = (act_coords[:, 1] / np.max(act_coords[:, 1])*max_x).astype(int)
        act_pix_coords[:, 1] = (act_coords[:, 0] / np.max(act_coords[:, 0])*max_y).astype(int)  # corrected to use act_coords[:, 0]
        # Prepare an image cube to store the influence functions.
        img_cube = np.zeros((max_x, max_y, n_acts))
        amps = np.ones(n_acts)
        # For each actuator, compute the influence function with a TPS interpolation.
        for k in range(n_acts):
            print(f"{k+1}/{n_acts}", end='\r', flush=True)
            # Create a command vector with a single nonzero element.
            act_data = np.zeros(n_acts)
            act_data[k] = amps[k]
            tps = ThinPlateSpline(alpha=0.0)
            tps.fit(act_pix_coords, act_data)
            flat_img = tps.transform(pix_coords)
            img_cube[:, :, k] = flat_img.reshape((max_x, max_y))
        # Create a cube mask that tiles the local mirror mask for each actuator.
        cube_mask = np.tile(self.mask, n_acts).reshape(img_cube.shape, order='F')
        cube = np.ma.masked_array(img_cube, mask=cube_mask)
        # Save the cube to a FITS file.
        fits_file = fp.INFLUENCE_FUNCTIONS_FILE(self.nActs)
        osu.save_fits(fits_file, cube)
        self._iffCube = cube

    def _scaleActCoords(self):
        """
        Scales the actuator coordinates to the mirror's pixel scale.
        """
        max_x, max_y = self.mask.shape
        act_coords = self.actCoords.T  # shape: (n_acts, 2)
        act_pix_coords = np.zeros((self.nActs,2), dtype=int)
        act_pix_coords[:, 0] = (act_coords[:, 1] / np.max(act_coords[:, 1])*max_x).astype(int)
        act_pix_coords[:, 1] = (act_coords[:, 0] / np.max(act_coords[:, 0])*max_y).astype(int)
        return act_pix_coords