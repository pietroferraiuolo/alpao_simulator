import numpy as _np
import matplotlib.pyplot as _plt
from alpao_simulator.ground import geometry as _geo
from alpao_simulator.ground import zernike as zern
from alpao_simulator.ground import config_loader as _cl
from matplotlib.animation import FuncAnimation as _FuncAnimation


class Interferometer:

    def __init__(self, dm):
        self.model = "4DAccuFiz"
        self.full_frame = False
        self.shapesRemoved = None
        self._dm = dm
        self._lambda = 632.8e-9  # Wavelength of the light in meters
        self._anim = None
        self._live = False
        self._surf = False
        self._fW, self._fH = self._readFullFrameSize()

    def live(
        self,
        shape2remove=None,
        noisy: bool = False,
        update_interval: int = 100,
        wavefront: bool = True,
        **kwargs,
    ):
        """
        Runs the live-view animation for the simulated Interferometer
        instance.

        Parameters
        ----------
        shape2remove : np.array, optional
            Zernike modes to be removed from the wavefront.
        **kwargs : dict, optional
            Additional keyword arguments for customization.

        Returns
        -------
        fig : matplotlib.figure.Figure
            Figure object of the live-view animation.
        anim : matplotlib.animation.FuncAnimation
            Animation object of the live-view animation (needed to keep the plot
            alive).
        """
        self._surf = not wavefront
        if shape2remove is not None:
            self.shapeRemoval(shape2remove)
        global _anim
        cmap = kwargs.get("cmap", "gray")

        self._live = True
        self._dm._live = True

        # Main plot creation
        _plt.ion()
        fig, ax = _plt.subplots(figsize=(7, 7.5))
        fig.subplots_adjust(top=0.9, bottom=0.1, left=0.05, right=0.95)
        fig.canvas.manager.set_window_title(f"Live View - Alpao DM {self._dm.nActs}")
        simg = self._dm._wavefront(zernike=shape2remove, wf=self._surf, noisy=noisy)
        if self.full_frame:
            simg = self.intoFullFrame(simg)
        im = ax.imshow(simg, cmap=cmap)
        ax.axis("off")
        fig.colorbar(im, ax=ax, orientation="horizontal", pad=0.05, shrink=0.9)
        pv_txt = fig.text(0.5, 0.1, "", ha="center", va="center", fontsize=15)
        shape_txt = fig.text(0.5, 0.925, "", ha="center", va="center", fontsize=15)
        fps_txt = fig.text(0.5, 0.1, "", ha="center", va="center", fontsize=15)

        # Closing Event
        def on_close(event):
            self._live = False
            self._dm._live = False

        fig.canvas.mpl_connect("close_event", on_close)

        # Update Event
        def update(frame):
            new_img = self._dm._wavefront(
                zernike=self.shapesRemoved, wf=self._surf, noisy=noisy
            )
            if self.full_frame:
                new_img = self.intoFullFrame(new_img)
            if not self._surf:
                fps_txt.set_text(f"FPS: {(1 / update_interval * 1000):.1f}")
                pv_txt.set_text("")
                shape_txt.set_text("")
            else:
                pv = (_np.max(new_img) - _np.min(new_img)) * 1e6
                rms = _geo.rms(new_img) * 1e6
                pv_txt.set_text(
                    r"PV={:.3f} $\mu m$".format(pv)
                    + " " * 10
                    + r"RMS={:.5f} $\mu m$".format(rms)
                )
                stext = (
                    f"Removing Zernike modes {self.shapesRemoved}"
                    if self.shapesRemoved is not None
                    else ""
                )
                shape_txt.set_text(stext)
                fps_txt.set_text("")
            im.set_clim(
                vmin=new_img.min(), vmax=new_img.max()
            )  # to not have blank plot
            im.set_data(new_img)
            return (im,)

        # Create and hold a reference to the animation.
        self._anim = _FuncAnimation(
            fig,
            func=update,
            interval=update_interval,
            blit=False,
            cache_frame_data=False,
        )
        _plt.show(block=False)

        # force an `update()` to update the figure
        _plt.pause(0.5)
        update(0)

        return fig, self._anim

    def acquire_phasemap(self, nframes: int = 1, rebin=1):
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
        if self.shapesRemoved is not None:
            fimage = zern.removeZernike(fimage, self.shapesRemoved)
        if self._live:
            self._surf = True
            _plt.pause(1)
            self._surf = False
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
        ocentre = (params["Width"] // 2 - 1, params["Height"] // 2 - 1)
        ncentre = (self._fW // 2 - 1, self._fH // 2 - 1)
        offset = (ncentre[0] - ocentre[0], ncentre[1] - ocentre[1])
        newidx = (self._dm._idx[0] + offset[0], self._dm._idx[1] + offset[1])
        full_frame = _np.zeros((self._fW, self._fH))
        full_frame[newidx] = img.compressed()
        new_mask = full_frame == 0
        full_frame = _np.ma.masked_array(full_frame, mask=new_mask)
        return full_frame

    def shapeRemoval(self, modes):
        """
        Removes the acquired shape by the define Zernike modes.

        Parameters
        ----------
        modes : np.array
            Modes to be filtered out.
        """
        self.shapesRemoved = modes

    def continuous(self):
        """
        Continuously acquires the phase map of the interferometer.

        In reality, instead of the fringes, it will show the surface
        shape acquired of the dm.
        """
        self._surf = True if self._surf is False else False

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
        params["Width"] = int(data["width"])
        params["Height"] = int(data["height"])
        params["x-offset"] = int(data["x-offset"])
        params["y-offset"] = int(data["y-offset"])
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
        return (int(data["full_width"]), int(data["full_height"]))
