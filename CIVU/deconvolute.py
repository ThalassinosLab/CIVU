"""Main module of Deconvolution package. 

Alter this module's main() function to run. Options are described in the main() 
and deconvolve() functions.

Created by Simos Kalfas
    email:simos.kalfas@gmail.com
    github: https://github.com/simoskalfas/
"""

import parse
import os
import smoother
import utils
import analyse
import optimisation
import time
import argparse

def deconvolve(filename, res_filename, smooth, mean_mode, title, xticks, 
    ciu, cycles, aline, print_res=True,):
    """Handles deconvolution and result processing

    Works as a control center for the package, handling all processes and 
    output.
    
    Args:
        filename: Data file name without file extension
        res_filename: Identifier for result file names
        smooth: Moving average smoothing factor in format: 
            [window size, interval]. No smoothing if left empty
        mean_mode: 'der' for second derivative
                   'rel_max' for relative maxima
                   [mean1, mean2, ... ] for given means, where mean is float 
                        for x-axis value, int for index
                   [] to return unfitted data
        cycles: Number of optimisation iterations.
        print res: If True returns plots and error log, in a folder one level 
                above.
                   If False returns dict with parameters for deconvoluted peaks 
                for each ATD
        aline(optional): If True all data will be alined according to the 
            smallest x value for a global maximum in the dataset

    Returns:
        If print_res is False:
           retdic: Dictionary with fitted parameters and errors"""
    datadic = parse.handle_file(filename)
    if aline:  #Aline file if desired
        datadic = parse.aline(parse.handle_file(filename), filename)
    arrival_time = datadic[filename]
    av_error = []
    areas = []
    fwhms = []
    retdic = {}
    #Create results folder
    script_dir = os.path.abspath(os.path.join(__file__, "../.."))
    results_dir = os.path.join(script_dir, filename + res_filename + '/')
    if not os.path.isdir(results_dir):
        os.makedirs(results_dir)
    #Create error log file
    with open(results_dir + filename + res_filename + '_errorlog_' + str(cycles) 
            + '.txt', 'w') as f:
        for key in sorted(datadic): #Loop over ATDs
            voltage = key
            if voltage == filename: #Exclude arrival times
                continue
            print voltage
            intensities = list(smoother.smooth(datadic[voltage], smooth)) 
            norm_factor = 100 / max(intensities) #Scale factor for normalisation
            means = utils.find_means(intensities, arrival_time, mean_mode)  
            means.sort()
            print 'Mean indices: ' + str(means)
            initial_sds = [0.01 for _ in range(len(means))]
            initial_heights = [intensities[i] for i in means]
            fitted_parameters_f, fit_f, fitted_parameters_r, fit_r = optimisation.run_opt_cycles(
                                        cycles, arrival_time, intensities,
                                        initial_sds,initial_heights, means)
            av_par, gausslist, min_er, error = analyse.list_of_gaus(
                                arrival_time, intensities, fitted_parameters_f,
                                            fitted_parameters_r, norm_factor)
            av_error.append(min_er) #For final average error calculation
            areacur = []
            fwhmcur = []
            total_area = utils.auc(intensities, arrival_time) * norm_factor
            erind = error.index(min_er)
            #For area under the curve plot
            for i in range(len(gausslist[erind]) - 2):
                areacur.append(((utils.auc(gausslist[erind][i], arrival_time) * 
                    norm_factor) / total_area) * 100)
            #For full width half maximum plot
            for i in range(len(gausslist[erind]) - 2):
                fwhmcur.append(utils.fwhm(gausslist[erind][i][2]))
            areas.append(areacur)
            fwhms.append(fwhmcur)
            if print_res: #Create plots and error log
                f.write(key + '\n')
                f.write(str(error[0]) + ' forward error' + '\n')
                f.write(str(error[1]) + ' reverse error' + '\n')
                f.write(str(error[2]) + ' average error' + '\n')
                f.write('\n\n\n')
                f.write('Average gaussian parameters:\n\n')
                f.write(str(erind) + '\n\n')
                f.write('Intenity\tMean\tSd\n')
                for i in av_par:
                    f.write(str(i))
                    f.write('\n')
                f.write('\n\n\n\n')
                #utils.plot_things is a versatile plotting function
                utils.plot_things(arrival_time, [gausslist[erind]], filename, 
                    voltage, res_filename, title, ciu)
            # else: #Make dict output with parameters and error values
            #     erlist = error
            #     parlist = fitted_parameters_f
            #     minind = erlist.index(min(erlist))
            #     retdic[voltage] = []
            #     retdic[voltage].append(means)
            #     retdic[voltage].append(parlist[minind])
            #     retdic[voltage].append(erlist[minind])
            #     retdic[voltage].append([fit_f, fit_r, fit_av][minind])
        if print_res: #Return results concerning full CIU: area plot, FWHM plot
            analyse.results(f, av_error, areas, fwhms, datadic, results_dir, 
                filename, res_filename, title, xticks)
            print av_error
        else:
            return retdic


def main():
    #Start timer to measure time to completion
    start_time = time.time()
    parser = argparse.ArgumentParser(description="""Gaussian deconvolution of 
    	arrival time distributions.""")
    parser.add_argument('filename', type=str, help="""Data file (.txt format). 
    	Has to be in a folder named "Data" one level above the script.""")
    parser.add_argument('title', type=str, help="""Additional title printed on 
    	plots""")
    parser.add_argument('mean_mode', help="""Mode of mean determination: \n
  					'der' for automatic determination with second derivative 
  					method, \n
  					'rel_max' for relative maxima to be taken as the means, \n
  					list of float for numerical means, \n
  					list of integers for indices.""")
    parser.add_argument('directory_label', type=str, help="""Label for results
    	directory which will be created a level above the script""")
    parser.add_argument('-s', '--smooth', default=[], type=list, metavar='',
    	help="""[window size, interval]. If not included or empty there will be 
    	no smoothing.""")
    parser.add_argument('-x', '--xlabels', default=[], type=list, metavar='', 
    	help="""Labels for x-axis of the area tracking plot (optional). Leave 
    	empty no x-axis labels. Should be given as a list of numbers.""")
    parser.add_argument('-c', '--not_ciu', action='store_true', 
    	help="""Include if data is not CIU.""")
    parser.add_argument('-r', '--repeats', default=5, type=int, metavar='', 
    	help="""Number of recursions (depth of analysis). Default (recommended) 
    	is 5.""")
    parser.add_argument('-a', '--align', action='store_true',  
    	help="""Include if the data should be aligned.""")
    args = parser.parse_args()
    # #Input filename of data file here without file extension
    if (args.mean_mode)[0] != '[':
		means = args.mean_mode
    elif any([i for i in args.mean_mode if i =='.']):
		means = [float(i) for i in args.mean_mode[1:-1].split(',')]	
    else:
		means = [int(i) for i in args.mean_mode[1:-1].split(',')]	
    print means 
    filename = args.filename[:-4]
    title = args.title
    # #Identifier for result file
    res_filename = args.directory_label
    # #Moving average smoothing in format: [window size, interval]. No smoothing 
    # #if left empty
    smooth = []
    if args.smooth != smooth:
    	smooth = [int(i) for i in args.smooth if unicode(i).isnumeric()]
    # #Ticks for data on the area under the curve plot. Should correspond to the
    # #voltages of the ATDs in the dataset.
    xticks = [] 
    if args.xlabels != xticks:
    	xticks = [int(i) for i in args.xlabels if unicode(i).isnumeric()]
    # #Mode of mean determination: 'der' for second derivative, 'rel_max' for 
    # #relative maxima, [int, ..., int] for indices, [float, ..., float] for 
    # #numerical
    ciu = not args.not_ciu
    cycles = args.repeats
    aline = args.align
    #If analysing a CIU dataset change ciu to True and aline to False.
    deconvolve(filename, res_filename, smooth, means, title, xticks, ciu, 
        cycles, aline)
    print time.time() - start_time
    print 'full time elapsed'


if __name__ == '__main__':
    main()