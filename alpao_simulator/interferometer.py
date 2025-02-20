import time as _t
import numpy as _np
import matplotlib.pyplot as _plt
from alpao_simulator.ground import geometry as _geo
from alpao_simulator.ground import config_loader as _cl
from matplotlib.animation import FuncAnimation as _FuncAnimation

class Interferometer:

    def __init__(self, dm):
        self._dm = dm
        self.model = "4DAccuFiz"
        self._lambda = 632.8e-9 # Wavelength of the light in meters
        self._fullWidth, self._fullHeight = self._readFullFrameSize()
        self._anim = None
        self._live = False
        self.full_frame = False


    def live(self, update_interval: int = 250, with_profiles: bool = False, **kwargs):
        """
        Runs the live-view animation for the simulated Interferometer
        instance.

        Parameters
        ----------
        dm : Object
            An instance of the deformable mirror to display it's surface.
        update_interval : float
            Time interval in milliseconds between updates.
        with_profiles : bool
            If True, the profile of the DM actuators is
            displayed alongside the wavefront.

        Returns
        -------
        fig : matplotlib.figure.Figure
            Figure object of the live-view animation.
        anim : matplotlib.animation.FuncAnimation
            Animation object of the live-view animation (needed to keep the plot
            alive).
        """
        cmap = kwargs.get('cmap', 'gray')
        self._live = True
        self._dm._live = True
        global _anim
        _plt.ion()
        if with_profiles:
            fig, ax = _plt.subplots(figsize=(9.5,10))
            fig.canvas.manager.set_window_title(f"Live View - Alpao DM {self._dm.nActs}")
            gs = fig.add_gridspec(2, 2,  width_ratios=(4, 1), height_ratios=(4, 1),
                            left=0.1, right=0.9, bottom=0.1, top=0.9,
                            wspace=0.025, hspace=0.025)
            # Wavefront image
            ax = fig.add_subplot(gs[0, 0])
            simg = self._dm._wavefront()
            if self.full_frame:
                simg = self.intoFullFrame(simg)
            im = ax.imshow(simg, cmap=cmap)
            ax.set_xticks([])
            ax.set_yticks([])
            # vertical profile
            axy = fig.add_subplot(gs[0, 1], sharey=ax)
            axy.set_yticks([])
            axy.hist(simg.compressed(), orientation='horizontal', histtype='step')
            axy.tick_params(axis='y', labelleft=False)
            # horizontal profile
            axx = fig.add_subplot(gs[1, 0], sharex=ax)
            axx.set_xticks([])
            axx.hist(simg.compressed(), orientation='vertical', histtype='step')
            axx.tick_params(axis='x', labelbottom=False)
            pv_text = fig.text(0.5, 0.05, "", ha="center", va="center", fontsize=15)
        else:
            fig, ax = _plt.subplots(figsize=(7,7.5))
            fig.canvas.manager.set_window_title(f"Live View - Alpao DM {self._dm.nActs}")
            simg = self._dm._wavefront()
            if self.full_frame:
                simg = self.intoFullFrame(simg)
            im = ax.imshow(simg, cmap=cmap)
            ax.axis('off')
            cbar = fig.colorbar(im, ax=ax, orientation='horizontal', pad=0.05, shrink=0.9)
            pv_text = fig.text(0.5, 0.05, "", ha="center", va="center", fontsize=15)
            fig.tight_layout()
        def on_close(event):
            self._live = False
            self._dm._live = False
        fig.canvas.mpl_connect('close_event', on_close)
        def update(frame):
            new_img = self._dm._wavefront()
            if self.full_frame:
                new_img = self.intoFullFrame(new_img)
            im.set_clim(vmin=new_img.min(), vmax=new_img.max()) ##
            im.set_data(new_img)
            pv = (_np.max(new_img) - _np.min(new_img))*1e6
            rms = _geo.rms(new_img)*1e6
            pv_text.set_text(r'PV={:.3f} $\mu m$'.format(pv)+' '*10+r'RMS={:.5f} $\mu m$'.format(rms))
            return im,
        update(0)
        # Create and hold a reference to the animation.
        self._anim = _FuncAnimation(
            fig,
            func=update,
            interval=update_interval,
            blit=False,
            cache_frame_data=False
        )
        _plt.show(block=False)
        # force an `update()` to update the figure
        _plt.pause(0.5)
        update(0)
        return fig, self._anim


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
        if self.full_frame:
            fimage = self.intoFullFrame(fimage)
        return fimage
    

    def intoFullFrame(self, img=None):
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
        if img is None:
            self.full_frame = True
            return
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
        data = _cl.load_interf_configuration(self.model)
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
        data = _cl.load_interf_configuration(self.model)
        return (int(data['full_width']), int(data['full_height']))
    