import numpy as np
from alpao_simulator.ground.base_deformable_mirror import BaseDeformableMirror

class AlpaoDm(BaseDeformableMirror):

    def __init__(self, nActs):
        super(AlpaoDm, self).__init__(nActs)
        self._shape = np.ma.masked_array(self.mask * 0, mask=self.mask, dtype=float)
        self._idx = np.where(self.mask == 0)
        self._actPos = np.zeros(self.nActs)


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
        self._actPos = command
        self._mirror_command(command, differential, modal)

    def get_shape(self):
        """
        Returns the current amplitudes commanded to the dm's actuators.

        Returns
        -------
        np.array
            Current amplitudes commanded to the dm's actuators.
        """
        return self._actPos
    
    def acquire_phasemap(self):
        """
        Acquires the phase map of the deformable mirror.
        
        Returns
        -------
        np.array
            Phase map of the deformable mirror.
        """
        image = np.ma.masked_array(self._shape, mask=self.mask)
        return image

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
        cmd_amps = cmd
        if modal: # convert modal to zonal
            shape = np.matmul(self.ZM, cmd)
            cmd_amps = np.matmul(self.RM, shape)
        if diff:
            cmd_amps = cmd_amps - self._actPos
            self._actPos += cmd_amps
        else:
            self._actPos = cmd_amps
        _cmd = cmd_amps - self._actPos if diff else cmd_amps
        self._shape[self._idx] += np.dot(self.IM.T, _cmd)
        
