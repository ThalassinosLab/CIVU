"""Contains functions used for moving average smoothing.


Created by Simos Kalfas and Charlie Eldrid
    email:simos.kalfas@gmail.com
    github: https://github.com/simoskalfas/
"""

import numpy as np


def movingaverage(interval, window_size):
    """Smooths a list with the moving average method.

    Args:
        interval: List to be smoothed
        window_size: Size of convolution window

    Returns:
        Smoothed list
    """
    window = np.ones(int(window_size)) / float(window_size)
    return np.convolve(interval, window, 'same')


def smooth(intensity, mode):
    """Loops and averages the sequential smoothing.

    Args:
        intensity: Arrival time series.
        mode: Number of repeats and window size. If empty, returns the given 
            list.
                [number, window] 
    """
    if not mode:
        return intensity
    intensity_output = []
    intensity_smooth = []
    mean_smooth_counter = mode[0]
    while mean_smooth_counter >= 1:
        window_smooth = mode[1]
        if len(intensity_output) == 0:
            intensity_array = np.array(intensity)
            intensity_smooth = movingaverage(intensity_array, window_smooth)
            mean_smooth_counter = mean_smooth_counter - 1
            intensity_output = intensity_smooth
        else:
            intensity_smooth = movingaverage(intensity_output, window_smooth)
        mean_smooth_counter = mean_smooth_counter - 1
    return intensity_smooth


def main():
    return


if __name__ == '__main__':
    main()
