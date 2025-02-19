import sys
import functools
import multiprocessing as mp
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

# Global variable so the animation reference is maintained.
_anim = None

def live_animation(dm, with_profiles: bool = False, update_interval=500):
    """
    Runs the live-view animation for an Interferometer instance.

    Parameters
    ----------
    dm : Object
        An instance of the deformable mirror to display it's surface.
    update_interval : float
        Time interval in milliseconds between updates.
    """
    global _anim
    plt.ion()

    fig, ax = plt.subplots()
    fig.canvas.manager.set_window_title(f"Live View - Alpao DM {dm.nActs}")
    im = ax.imshow(dm._wavefront(), cmap='gray_r')
    #ax.set_title(f"Alpao DM {dm.nActs}")
    if with_profiles:
        ax2 = fig.add_axes([0.1, 0.1, 0.3, 0.3])
        ax2.set_title("Profile")
        ax2.set_xlabel("Actuator")
        ax2.set_ylabel("Amplitude")
        ax2.set_xlim(0, dm.nActs)
        ax2.set_ylim(-1, 1)
        ax2.plot(dm.get_shape(), 'b-')
        ax2.grid(True)
    else:
        ax.axis('off')
    fig.tight_layout()

    def update(frame, dm):
        new_img = dm._wavefront()
        im.set_data(new_img)
        #fig.canvas.draw_idle()
        return im,

    # Create and hold a reference to the animation.
    _anim = FuncAnimation(
        fig,
        func=functools.partial(update, dm=dm),
        interval=update_interval,
        blit=False,
        cache_frame_data=False
    )
    plt.show()
    return fig, _anim
