import time as _t
import numpy as _np
from alpao_simulator.ground import geometry as _geo
from alpao_simulator.ground import config_loader as cl

class Interferometer:

    def __init__(self, dm):
        self._dm = dm
        self.model = "4DAccuFiz"
        self._lambda = 632.8e-9 # Wavelength of the light in meters
        self._fullWidth, self._fullHeight = self._readFullFrameSize()

    def acquire_phasemap(self, nframes:int=1, rebin=1):
        """
        Acquires the phase map of the interferometer.
        
        Returns
        -------
        np.array
            Phase map of the interferometer.
        """
        imglist = []
        for i in range(nframes):
            img = self._dm._shape
            kk = _np.floor(_np.random.random(1) * 5 - 2)
            masked_ima = img + _np.ones(img.shape) * self._lambda * kk
            imglist.append(masked_ima)
        image = _np.ma.dstack(imglist)
        image = _np.mean(image, axis=2)
        masked_img = _np.ma.masked_array(image, mask=self._dm.mask)
        fimage = _geo.rebinned(masked_img, rebin)
        return fimage
    

    def intoFullFrame(self, img):
        """
        Converts the image to a full frame image of 2000x2000 pxs.
        
        Parameters
        ----------
        img : np.array
            Image to be converted to a full frame.
            
        Returns
        -------
        full_frame : np.array
            Full frame image.
        """
        params = self.getCameraSettings()
        ocentre = (params['Width']//2-1, params['Height']//2-1)
        ncentre = (self._fullWidth//2-1, self._fullHeight//2-1)
        offset = (ncentre[0] - ocentre[0], ncentre[1] - ocentre[1])
        newidx = (self._dm._idx[0] + offset[0], self._dm._idx[1] + offset[1])
        full_frame = _np.zeros((self._fullWidth, self._fullHeight))
        full_frame[newidx] = img.compressed()
        new_mask = (full_frame == 0)
        full_frame = _np.ma.masked_array(full_frame, mask=new_mask)
        return full_frame


    def getCameraSettings(self):
        """
        Reads the configuration of the 4D interferometer.
        
        Returns
        -------
        dict
            Configuration file of the 4D interferometer.
        """
        data = cl.load_interf_configuration(self.model)
        params = {}
        params['Width'] = int(data['width'])
        params['Height'] = int(data['height'])
        params['x-offset'] = int(data['x-offset'])
        params['y-offset'] = int(data['y-offset'])
        return params
    
    def _readFullFrameSize(self):
        """
        Reads the full frame size of the 4D interferometer.
        
        Returns
        -------
        tuple
            Full frame size of the 4D interferometer.
        """
        data = cl.load_interf_configuration(self.model)
        return (int(data['full_width']), int(data['full_height']))
    