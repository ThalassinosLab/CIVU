# Package for the deconvolution of arrival time distributions.

This package aims to improve the analysis and presentation of the data produced by Ion Mobility Mass Spectrometry (IM-MS) and, more specifically, Collision Induced Unfolding (CIU). For details on these structural biology techniques, I would advise you to refer elsewhere. However, the functionalities provided by this project could be used in other fields where similar data is acquired.


The package's main function is to deconvolute series of 2-dimensional mixtures of Gaussian peaks and produce plots of the deconvoluted data, as well as an area under the curve plot for tracking populations over the data set. Note that if the number of Gaussian peaks fitted is not the same in the whole dataset, the are under the curve tracking plot will not be output.

## The data analysed.

A CIU assay produces a heatmap with voltage on the x-axis, arrival time on the y-axis and intensity as heat. An example can be seen below:

![](https://github.com/simoskalfas/CIVU/blob/master/Images/Heatmap.png)

The heatmap is made up of this kind of distributions (Arrival Time Distributions (ATDs)):

![](https://github.com/simoskalfas/CIVU/blob/master/Images/ATD.png)

The features of the heatmap are the experimental results that are analysed and presented. Until now, this analysis has relied on manual deconvolution and qualitative features, because the differences between analytes can be very small and the meaning of each such deviation is speculative.


The ATDs are sums (mixtures) of various Gaussian distributions that correspond to the entities present in the analyte solution. These entities evolve into each other bound by several physical rules. Since we only see the sum of these peaks, their relative abundancies and number are unknown. Getting quantitative information on these distributions would provide a more robust framework for CIU data analysis.


The main setback is that a 2D mixture of Gaussian distributions could be made up of a near-infinite number of sets of peaks. Getting a good automated deconvolution method is important, but the "correct" answer will always depend on the context of the data. In the future, this package might be adapted to specifically solve ATDs. For now, however, a recommended manual step is described below.

## Output examples.

The style of plot for a deconvoluted distribution is the following:

![](https://github.com/simoskalfas/CIVU/blob/master/Images/Example_deconv.png)

For the same CIU data set, the area under the curve (population tracking) plot looks like this:

![](https://github.com/simoskalfas/CIVU/blob/master/Images/Example_areas.png)

## Installation and use.

This package can be manually installed into the python package directory. However, the recommended use is as a script package through the CLI described here.


All the necessary modifications for running the package on a CIU data set are in the main() function of the Deconvolute_main module. Specific instructions are commented in the code itself. To analyse different types of data you will need to alter the functions in the parse module, but keep in mind that different data is not necessarily supported, so more modifications might be necessary.


The package also expects a specific file architecture. The data file(s) have to be in a folder parallel to the folder containing the code named 'Data' the resulting plots will be in a new folder, also parallel to the others. It is reommended to edxactly replicate the architecture of the package as downloaded (replace the demo data with yours).

## The Command Line Interface 

The script should be run in the following fashion: 
'''
python Deconvolute_main.py <'datafile.txt'> <'plot title'> <mean determination> <'result label'> '''
For more options run with '-h'

The mean determination argument can take the following input:
- 'der' for automatic mean estimation using the second derivative.
- 'rel_max' for simple datasets where the relative maxima of the curve are likely to accurately reflect the positions of the peaks.
- list of integers [mean1, mean2, ...] for a list of specific indices of the full curve to be used as means (recommended for manually tuning the means).
- list of float [mean1, mean2, ...] for a list of specific numbers along the x-axis to be used as mean positions (not as easy to tune except if bin number makes the data pseudo-continuous).

## Recommended protocol

- Run on second derivative mode (set mean determination to 'der'). The errors for each ATD and parameters for every Gaussian peak fitted will be printed in the form [height, mean, standard deviation].
- Chose the best fitted ATD. Copy the means of the significant peaks into the mean determination argument (as list) and run again. A good cutoff for peak significance is to drop the ones with numerical values more than two orders of magnitude less than that of the highest peak. The means as indices will also be printed in the same order as the parameters for each corresponding peak.
- Tune the means until they fit all distributions as closely as possible. It is recomended to work with the means in index form that are printed when the script is run.

## Testing.

Downloading the whole repository and running Deconvolute_main will analyse Demo_data_1.txt in the Data folder. More such examples of experimental data are available in the same folder for demonstration purposes.

