import os
import numpy as np
from matplotlib import pyplot as plt
from alpao_simulator import folder_paths as fp
from alpao_simulator.ground import osutils as osu
from alpao_simulator.ground.base_deformable_mirror import BaseDeformableMirror

class AlpaoDm(BaseDeformableMirror):

    def __init__(self, nActs):
        super(AlpaoDm, self).__init__(nActs)
        self.cmdHistory = None
        self._shape = np.ma.masked_array(self.mask * 0, mask=self.mask, dtype=float)
        self._idx = np.where(self.mask == 0)
        self._actPos = np.zeros(self.nActs)
        self._live = False


    def set_shape(self, command, differential:bool=False, modal:bool=False):
        """
        Applies the given command to the deformable mirror.
        
        Parameters
        ----------
        command : np.array
            Command to be applied to the deformable mirror.
            
        differential : bool
            If True, the command is applied differentially.
        """
        self._mirror_command(command, differential, modal)
        if self._live:
            import time
            time.sleep(0.15)
            plt.pause(0.05)

    def get_shape(self):
        """
        Returns the current amplitudes commanded to the dm's actuators.

        Returns
        -------
        np.array
            Current amplitudes commanded to the dm's actuators.
        """
        return self._actPos.copy()
    
    def uploadCmdHistory(self, cmdhist):
        """
        Upload the command history to the deformable mirror memory.
        Ready to run the `runCmdHistory` method.
        """
        self.cmdHistory = cmdhist

    def runCmdHistory(self, interf=None, rebin:int=1, save:bool=False):
        """
        Runs the command history on the deformable mirror.
        
        Parameters
        ----------
        interf : Interferometer
            Interferometer object to acquire the phase map.
        rebin : int
            Rebinning factor for the acquired phase map.
        save : bool
            If True, saves the acquired phase maps.
            
        Returns
        -------
        tn :str
            Timestamp of the data saved.
        """
        if self.cmdHistory is None:
            raise Exception("No Command History to run!")
        else:
            tn = osu.newtn()
            print(f"{tn} - {self.cmdHistory.shape[-1]} images to go.")
            datafold = os.path.join(fp.OPD_IMAGES_FOLDER, tn)
            if not os.path.exists(datafold):
                os.mkdir(datafold)
            for i,cmd in enumerate(self.cmdHistory.T):
                print(f"{i+1}/{self.cmdHistory.shape[-1]}", end="\r", flush=True)
                self.set_shape(cmd)
                if interf is not None:
                    img = interf.acquire_phasemap(rebin=rebin)
                    path = os.path.join(datafold, f"image_{i:05d}.fits")
                    osu.save_fits(path, img)
        self.set_shape(np.zeros(self.nActs))
        return tn

    def visualize_shape(self, cmd=None):
        """
        Visualizes the command amplitudes on the mirror's actuators.

        Parameters
        ----------
        cmd : np.array, optional
            Command to be visualized on the mirror's actuators. If none, will plot
            the current position of the actuators.

        Returns
        -------
        np.array
            Processed shape based on the command.
        """
        if cmd is None:
            cmd = self._actPos.copy()
        plt.figure(figsize=(7, 6))
        size = (120*97)/self.nActs
        plt.scatter(self._scaledActCoords[:,0], self._scaledActCoords[:,1], c=cmd, s=size)
        plt.xlabel(r"$x$ $[px]$")
        plt.ylabel(r"$y$ $[px]$")
        plt.title(f"DM {self.nActs} Actuator's Coordinates")
        plt.colorbar()
        plt.show()

    def _mirror_command(self, cmd, diff, modal):
        """
        Applies the given command to the deformable mirror.
        
        Parameters
        ----------
        cmd : np.array
            Command to be processed by the deformable mirror.
        
        diff : bool
            If True, process the command differentially.
        
        Returns
        -------
        np.array
            Processed shape based on the command.
        """
        if modal:
            mode_img = np.dot(self.ZM, cmd)
            cmd = np.dot(mode_img, self.RM)
        cmd_amp = cmd
        if not diff:
            cmd_amp = cmd - self._actPos
        self._shape[self._idx] += np.dot(cmd_amp, self.IM)
        self._actPos += cmd_amp


    def _wavefront(self):
        """
        Current shape of the mirror's surface. Only used for the interferometer's
        live viewer (see `interferometer.py`).
        
        Returns
        -------
        np.array
            Phase map of the interferometer.
        """
        return np.ma.masked_array(self._shape, mask=self.mask)