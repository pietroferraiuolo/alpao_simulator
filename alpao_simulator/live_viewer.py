import sys
import multiprocessing as mp
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

# Global variable so the animation reference is maintained.
_anim = None

def _live_animation(interferometer, update_interval):
    """
    Runs the live-view animation for an Interferometer instance.

    Parameters
    ----------
    interferometer : Object
        An instance of Interferometer (or similar) that has acquire_phasemap().
    update_interval : float
        Time interval in milliseconds between updates.
    """
    global _anim

    fig, ax = plt.subplots()
    im = ax.imshow(interferometer.acquire_phasemap(), cmap='gray')

    # Set up a callback to exit when the figure is closed.
    def on_close(event):
        sys.exit(0)
    fig.canvas.mpl_connect('close_event', on_close)

    def update(frame):
        new_img = interferometer.acquire_phasemap()
        im.set_data(new_img)
        fig.canvas.draw_idle()
        return im,

    # Create and hold a reference to the animation.
    _anim = FuncAnimation(
        fig,
        update,
        interval=update_interval,
        blit=False,
        cache_frame_data=False
    )
    plt.show()


def start_live_view(interferometer, update_interval=500):
    """
    Launches the live view animation in a new process.
    
    Parameters
    ----------
    interferometer : Object
        An instance of Interferometer.
    update_interval : float, optional
        Time interval in milliseconds between updates (default is 500ms).
    """
    p = mp.Process(target=_live_animation, args=(interferometer, update_interval))
    p.daemon = True
    p.start()


def liveView(interferometer, update_interval: float = 500):
    """
    Starts a live view that continuously updates the displayed phase map.
    The live view stops updating when the plot window is closed.
    
    Parameters
    ----------
    update_interval : float
        Time interval in milliseconds between updates.
    """
    start_live_view(interferometer, update_interval)