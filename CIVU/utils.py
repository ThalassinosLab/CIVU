"""Contains general utility functions used by the rest of the package.


Created by Simos Kalfas
    email:simos.kalfas@gmail.com
    github: https://github.com/simoskalfas/
"""
import numpy as np
import numpy.ma as ma
from matplotlib import pyplot as plt
from scipy.signal import argrelmin, argrelmax
from scipy.integrate import trapz
import seaborn as sns
import itertools
import os
import math
import re



def rmsd(predicted, actual):
    """Calculates root mean square deviation error between two lists.

    Args:
        predicted: Expected answer
        actual: Approximation

    Returns:
        RMSD value
    """
    predicted = np.array(predicted)
    actual = np.array(actual)
    return np.sqrt(((predicted - actual) ** 2).mean())  #RMSD formula


def gaussian(x, a, b, s):
    """Creates Gaussian distribution with the given parameters.

    Args:
        x: Arrival time series
        a: Height 
        b: Mean 
        s: Standard deviation 

    Returns:
        y: Gaussian peak
    """
    y = []
    for i in x:
        y.append(a * np.exp(-((i - b) ** 2) / (2 * (s ** 2))))  
    return y


def mask_a(array, intervals):
    """#Masks array in the given regions (intervals).

    Args:
        array: List to be masked
        intervals: Intervals of mask - [[start, end], [start. end], ...]

    Returns:
        mar: Starting array masked at the given intervals
    """
    mar = np.array(array)
    mask = np.zeros((len(array)))
    for i in range(len(intervals)):
        for j in range(intervals[i][0], intervals[i][1]):
            mask[j] = 1
    mar = ma.array(mar, mask=mask)
    return mar


def plot_things(x, ylists, filename, voltage, ident, title, ciu):
    """Vesatile plotting function.

    Args:
        x: Arrival time series
        ylists: Lists to be plotted. Each nested list's contents will be plotted 
            at a separate set of axes in the same figure. 
                [[list1, list2, ...],[listn, listm, ...], ...]
        filename: Name of data file without file extension
        voltage: Voltage value to be used as label
        ident: Identifier for result file names

    Returns:
        Nothing
    """
    plt.close('all')
    fig = plt.figure()
    plotdic = {}
    for i in range(1, len(ylists) + 1):  #Make enough axes
        colours = itertools.cycle(sns.color_palette('husl', len(ylists[i - 1])))
        plotdic[str(i)] = fig.add_subplot(len(ylists), 1, i)
        plotdic[str(i)].plot(x, ylists[i-1][-2], color='b', label='Sum', 
                linewidth=1.8)
        plotdic[str(i)].plot(x, ylists[i-1][-1], color='r', label='Trace', 
                linewidth=1.8)
        for j in range(len(ylists[i - 1])-2): #Plot each data list in their axes
            plotdic[str(i)].plot(x, ylists[i-1][j], color='k', linewidth=0.5)
            plotdic[str(i)].fill_between(x, 0, ylists[i-1][j], 
                    color=colours.next(), label=str(j+1), alpha=0.5)
        plotdic[str(i)].legend()
        plotdic[str(i)].set_xlabel('Adjusted time (ms)')
        plotdic[str(i)].set_ylabel('Normalised intensity')
    if ciu==True:
        fig.suptitle(title + ' ' + voltage)
    else:
        fig.suptitle(title + ' ' + voltage[:-1] + 'ms')  #Make plot directory 
    script_dir = os.path.abspath(os.path.join(__file__, "../.."))
    results_dir = os.path.join(script_dir, filename + ident + '/')
    if not os.path.isdir(results_dir):
        os.makedirs(results_dir)
    fig.savefig(results_dir + filename + '_' + str(voltage) + '.png') 
    fig.savefig(results_dir + filename + '_' + str(voltage) + '.svg') 
    return


def fwhm(sd):
    """Calculates full width half maximum of a normal distribution.

    Args:
        sd: Standard deviation of Gaussian peak.

    Returns:
        Full width half maximum value.
    """
    return 2 * np.sqrt(2 * (math.log(2))) * sd 


def auc(curve, arrival_times):
    """Calculates area under the curve of a normal distribution.

    Args:
        curve: Gaussian peak intensity values
        arrival_times: Arrival time series

    Returns:
        area: Area under the curve value
    """
    dx = arrival_times[1]
    area = trapz(curve, dx=dx) 
    return area


def mean_converter(means, arrival_times):
    """Converts numerical values to indices along a list.

    Args:
        means: Nmerical means to be converted
        arrival_times: Arrival time series

    Returns:
        retl: Means converted to indices
    """
    times = arrival_times[::]
    retl = []
    for i in means:
        times.append(i)
        times.sort()
        retl.append(times.index(i))
        times.pop(retl[-1])
    #print retl
    return retl


def find_means(data, xvals, mode):
    """Finds means of a distribution.

    A different method will be used acording to the value and type of the mode
    argument. See options below. It is very important to understand the 
    different modes before using the package.

    Args:
        data: Intensity values.
        xvals: Arrival time series.
        mode: 'der' for second derivative method.
              'rel_max' for relative maxima method.
               List of int for given means in index form.
               List of float for given numerical means.
               Empty list to produce plots of the data set.

    Returns:
        means: List of means in the form of indices on the x-axis
    """
    if mode == list(mode):
        if isinstance(mode[0], float):
            return mean_converter(mode, xvals)
        else:
            return mode
    elif mode == 'der':
        means = list(argrelmin(np.gradient(np.gradient(data)))[0])
        return means
    elif mode == 'rel_max':
        means = argrelmax(np.array(data), order=1)[0]
        return means

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    '''
    return [ atoi(c) for c in re.split('(\d+)', text) ]

def main():
    return


if __name__ == '__main__':
    main()
