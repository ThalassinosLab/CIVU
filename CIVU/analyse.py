"""Contains functions for analysis and presentation of results.


Created by Simos Kalfas
    email:simos.kalfas@gmail.com
    github: https://github.com/simoskalfas/
"""

import utils
import time
import numpy as np
from operator import add
from matplotlib import pyplot as plt
import itertools
import seaborn as sns


def weighted_average(forward, reverse):
    """Combines forward and reverse fitting results.

    In each direction of fitting, the quality of the fit will be declining due 
    to error propagation. The averaging is thus weighted to increase the 
    significance of the first fits from each method - the low arrival time for 
    the forward and the high arrival time for the reverse.
    
    Args:
        forward: Parameters for fitted peaks of the forward method
        reverse: Parameters for fitted peaks of the reverse method

    Returns:
        weighted_av: Averaged parameters
    """
    av_for = forward[::]
    av_rev = reverse[::]
    av_for = np.array(av_for)
    av_rev = np.array(av_rev)
    weights = np.linspace(0, 1, len(av_for)) #Weights in intervals from 0 to 1
    weights = [[weights[i] for _ in range(3)] for i in range(len(weights))]
    w_f = weights[::-1] #Forward weights from 1 to 0
    weights = np.array([w_f, weights])
    weighted_av = np.array([av_for, av_rev])
    if len(av_for) == 1: #If only one peak is present average without weights
        weighted_av = np.average(weighted_av, axis=0)
    else:
        weighted_av = np.average(weighted_av, axis=0, weights=weights)
    print weighted_av
    return weighted_av


def list_of_gaus(arrival_time, intensities, fitted_parameters_f, 
        fitted_parameters_r, norm_factor):
    """Parses results into a master nested list used for presentation and 
    evaluation. Also parses error information.

    Args:
        arrival_time: Arrival time series
        intensities: ATD curve (distribution)
        fitted_parameters_f: Parameters for fitted peaks of the forward method 
                [[height1, mean1, sd1],...]
        fitted_parameters_r: Parameters for fitted peaks of the reverse method 
                [[height1, mean1, sd1],...]
        norm_factor: Scale factor for unnormalised data

Returns:
        gausslist: List of gaussian distributions for each fitting method 
                [[average], [forward], [reverse]]
        min_error: Minimum error between fitting methods
        errorlist: List of error values 
                [forward, reverse, average]
    """
    average = weighted_average(fitted_parameters_f, fitted_parameters_r, ) 
    average = list(average)
    average = [list(i) for i in average]
    gausslist = [[], [], []] #[[average], [forward], [reverse]]
    for i in range(len(fitted_parameters_r)):
        gausslist[2].append(utils.gaussian(arrival_time, 
                *fitted_parameters_r[i]))
        gausslist[1].append(utils.gaussian(arrival_time, 
                *fitted_parameters_f[i]))
    for i in range(len(average)):
        gausslist[0].append(utils.gaussian(arrival_time, *average[i]))
    #Get sum of fitted peaks to compare to ATD curve
    fit_av = list(np.zeros((200)))
    fit_f = list(np.zeros((200)))
    fit_r = list(np.zeros((200)))
    for i in gausslist[0]:
        fit_av = map(add, fit_av, i)
    for i in gausslist[1]:
        fit_f = map(add, fit_f, i)
    for i in gausslist[2]:
        fit_r = map(add, fit_r, i)
    #The last element of each list in gausslist is the ATD curve and the second 
    #last the fit produced from the respective method
    gausslist[2].append(fit_r)
    gausslist[1].append(fit_f)
    gausslist[0].append(fit_av)
    gausslist[2].append(intensities)
    gausslist[1].append(intensities)
    gausslist[0].append(intensities)
    #Calculate errors normalising with scaling factor
    error_f = utils.rmsd(fit_f, intensities) * norm_factor
    error_r = utils.rmsd(fit_r, intensities) * norm_factor
    error_av = utils.rmsd(gausslist[0][-2], intensities) * norm_factor
    errorlist = [error_av, error_f, error_r]
    min_error = min(errorlist) 
    erind = errorlist.index(min_error)
    parlist = [average, fitted_parameters_f, fitted_parameters_r]
    return parlist[erind], gausslist, min_error, errorlist


def results(f, av_error, areas, fwhms, datadic, results_dir, filename, 
        res_filename, title, xticks):
    """Produces plots for presentation of the results.

    Args:
        f: Error log file already open when this function is called
        av_error: Global average error
        areas: Data for area under the curve plot
        fwhms: Data for FWHM plot
        datadic: Dictionary of parsed data
        results_dir: Results directory name
        filename: File name of data file without file extension
        res_dilename: Identifier for result file names

        Returns:
            Nothing
    """
    av_error = np.average(av_error)
    f.write(str(av_error)) #Write average error to error log
    fig2 = plt.figure() #Make area under the curve figure
    ax2 = fig2.add_subplot(1, 1, 1)
    areas = np.array(areas)
    areas = np.transpose(areas)
    colours = itertools.cycle(sns.color_palette('husl', len(areas)))
    for i in range(len(areas)):
        ax2.plot(np.sort([int(sorted(datadic)[j][:-1]) for j in range(
                len(areas[i]))]), areas[i], color=colours.next(), label=i+1)
    ax2.legend()
    ax2.set_xlabel('Activation energy (V)')
    ax2.set_ylabel('Percentage area under the curve')
    ax2.set_xticks(xticks)
    fig2.suptitle(title + ' population tracking')
    fig2.savefig(results_dir + filename + res_filename + '_areas.png')
    fig2.savefig(results_dir + filename + res_filename + '_areas.svg')
    return


def main():
    return


if __name__ == '__main__':
    main()
