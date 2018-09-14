"""Module containing methods needed for optimisation.

This optimiser uses the __ method as described in wiki but was developed from
scratch using few high level libraries.

Created by Simos Kalfas
    email:simos.kalfas@gmail.com
    github: https://github.com/simoskalfas/
""" 

import time
import utils
from operator import add



def windowmaker(x, means, direction):
    """Determines windows of optimisation for each peak in the spectrum.
    
    Args:
        x: Arrival time series
        means: The means of the current ATD as indices (int)
        direction: 'f' for forward optimisation
                   'r' for reverse optimisation

    Returns:
        windowlist: List of windows in format [[start index, end index], ...]
    """
    windowlist = []
    if direction == 'f':
        for i in range(len(means)):
            windowlist.append([0, means[i] + 3])
        return windowlist
    elif direction == 'r':
        for i in range(len(means)):
            windowlist.append([means[i], len(x)])
        return windowlist[::-1]


def run_opt_cycles(num, x, goal, initial_sd, initial_h, means, threshold=0):
    """Handles iterative optimisation.

    Each cycle entails optimisation of the standard deviation for each peak
    sequentially and then optimisation of the heights in the same fashion. The 
    results differ if the sequence of optimisation is ascending or descending.
    The two approximations are therefore averaged.
    
    Args:
        num: Number of cycles.
        x: Arrival time series.
        goal: Given distribution.
        initial_sd: Initial standard deviation values.
        initial_h: Initial height values.
        means: Mean values.
        threshold: Error threshold to stop optimisation. If left 0 the cycles 
            will run to the iteration limit.

    Returns:
        fitted_parameters_f: Parameters for forward Gaussian peaks.
            [[height1, mean1, sd1], ...]
        fit_f: Sum of fitted peaks for forward method
        fitted_parameters_r: Parameters for reverse Gaussian peaks.
            [[height1, mean1, sd1], ...]
        fit_r: Sum of fitted peaks for reverse method
    """
    opt_time = time.time()
    sd_f = initial_sd[::]
    heights_f = initial_h[::]
    #Standard deviations are optimised with initial height values.
    fitted_parameters_f, fit_f = optimiser(x, goal, sd_f, heights_f, means,
            threshold, 'sd', 'f')
    sd_f = [s[2] for s in fitted_parameters_f] #Update values
    sd_r = initial_sd[::]
    heights_r = initial_h[::]
    fitted_parameters_r, fit_r = optimiser(x, goal, sd_r, heights_r, means, 
            threshold, 'sd', 'r')
    sd_r = [s[2] for s in fitted_parameters_r]
    for _ in range(num):
        fitted_parameters_f, fit_f = optimiser(x, goal, sd_f, heights_f, means, 
                threshold, 'h', 'f')
        heights_f = [h[0] for h in fitted_parameters_f]
        fitted_parameters_f, fit_f = optimiser(x, goal, sd_f, heights_f, means, 
                threshold, 'sd', 'f')
        sd_f = [s[2] for s in fitted_parameters_f]
        fitted_parameters_r, fit_r = optimiser(x, goal, sd_r, heights_r, means, 
                threshold, 'h', 'r')
        heights_r = [h[0] for h in fitted_parameters_r]
        fitted_parameters_r, fit_r = optimiser(x, goal, sd_r, heights_r, means, 
                threshold, 'sd', 'r')
        sd_r = [s[2] for s in fitted_parameters_r]
    print 'optimisation time = ' + str(time.time() - opt_time)
    return fitted_parameters_f, fit_f, fitted_parameters_r, fit_r


def optimiser(x, curve, sd, heights, mean_indices, threshold, parameter, direction):
    """Main optimisation function.

    Optimises the value of the chosen parameter with the rest constant. The main
    loop can be changed to allow for more iterations. However, this is rarely 
    useful except if the iteration step is drastically reduced.
    
    Args:
        x: Arrival time series
        curve: Given distribution
        sd: Initial sd values
        heights: Initial height values
        mean_indices: Indices of means on x value list
        threshold: Error threshold to stop optimisation
        parameter: 'sd' to optimise standard deviation
                   'm' to optimise mean
                   'h' to optimise height
        direction: 'f' for forward optimisation
                   'r' for reverse optimisation

    Returns:
        parameter_lists: List of optimised parameters 
            [[height1, mean1, sd1], ...]
        fit: Sum of fitted gaussians
"""
    windows = windowmaker(x, mean_indices, direction) #Create windows
    num_means = [x[i] for i in mean_indices]  #Get numerical means
    norm_factor = 100 / max(curve)  #Scale factor for unnormalised data
    if parameter == 'sd':
        optimisation_index = 2
        fluctuation_factor = 0.01
    elif parameter == 'm':
        optimisation_index = 1
        fluctuation_factor = 0.2
    elif parameter == 'h':
        optimisation_index = 0
        fluctuation_factor = 0.5 / norm_factor #Scaled iteration step 
    parameter_lists = [[heights[i], num_means[i], sd[i]] for i in 
            range(len(heights))]
    if direction == 'r':
        parameter_lists = parameter_lists[::-1]
    fit = [0 * value for value in curve]
    prev_params = []
    for i in range(len(parameter_lists)): #Iterate over peaks
        params = parameter_lists[i]
        cur_gaussian = utils.gaussian(x, *params)
        cur_fit = map(add, fit, cur_gaussian)
        cur_window_opt = curve[windows[i][0]:windows[i][1]]
        error = utils.rmsd(cur_fit[windows[i][0]:windows[i][1]], cur_window_opt) 
        minimum_error = max(heights) * 100  #Initial value for minimum error 
        min_error_parameter = None  #Initial parameter value at the minimum error
        j = 0 
        prev_params = []
        while error > threshold and j < 201:
            if j == 200: #Iteration limit
                params[optimisation_index] = min_error_parameter
                cur_gaussian = utils.gaussian(x, *params)
                break
            up_par = params[optimisation_index] + fluctuation_factor
            up_params = params[::]
            down_par = params[optimisation_index] - fluctuation_factor
            if down_par <= 0: #Ensuring the parameter values stay over 0
                down_par = up_par
            if parameter == 'h': #Ensuring height does not exceed maximum
                if up_par > max(curve):
                    up_par = down_par
            up_params[optimisation_index] = up_par
            up_gaus = utils.gaussian(x, *up_params)
            down_params = params[::]
            down_params[optimisation_index] = down_par
            down_gaus = utils.gaussian(x, *down_params)
            up_cur_fit = map(add, fit, up_gaus)
            down_cur_fit = map(add, fit, down_gaus)
            #Checking if incrementing down or up is better (gives lower error)
            if utils.rmsd(up_cur_fit[windows[i][0]:windows[i][1]], 
                cur_window_opt) > utils.rmsd(down_cur_fit[windows[i][0]:windows[i][1]],
                    cur_window_opt) and down_params[optimisation_index] > 0:
                params = down_params
            else:
                params = up_params
            cur_gaussian = utils.gaussian(x, *params) #Update current peak shape
            cur_fit = map(add, fit, cur_gaussian)   #Update current sum
            error = utils.rmsd(cur_fit[windows[i][0]:windows[i][1]], 
                    cur_window_opt) #Update current error
            if error < minimum_error: #Check if the current error is the minimum 
                minimum_error = error
                min_error_parameter = params[optimisation_index] #Update optimal 
            if j > 2 and prev_params[-2] == params[optimisation_index]:
                params[optimisation_index] = min_error_parameter
                cur_gaussian = utils.gaussian(x, *params)
                break
            prev_params.append(params[optimisation_index])
            j += 1
        fit = map(add, fit, cur_gaussian)
        parameter_lists[i] = params
    if direction == 'r': #Reverse list for reverse results
        parameter_lists = parameter_lists[::-1]
    return parameter_lists, fit


def main():
    return


if __name__ == '__main__':
    main()
