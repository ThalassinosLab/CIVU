# Package for the deconvolution of arrival time distributions.

This package aims to improve the analysis and presentation of the data produced by Ion Mobility Mass Spectrometry (IM-MS) and, more specifically, Collision Induced Unfolding (CIU). For details on these structural biology techniques, I would advise you to refer elsewhere. However, the functionalities provided by this project could be used in other fields where similar data is acquired.
The package's main function is to produce plots of the deconvoluted data, as well as an area under the curve plot for tracking populations over the data set. Note that if the number of Gaussian peaks fitted is not the same in the whole dataset, the are under the curve tracking plot will not be output.

##The data analysed.

A CIU assay produces a heatmap with voltage on the x-axis, arrival time on the y-axis and intensity as heat. An example can be below:
![alt-text](link)
The heatmap is made up of this kind of distributions (Arrival Time Distributions (ATDs)):
![alt-text](link)
The features of the heatmap are the experimental results that are analysed and presented. This analysis, however, is done very quantitatively, because the significant differences can be very slight and the meaning of each such deviation is speculative.
The ATDs are sums (mixtures) of various Gaussian distributions that correspond to the entities present in the analyte solution. These entities evolve into each other bound by several physical rules. Since we only see the sum of these peaks, their relative abundancies is often not clear. Getting quantitative information on these distributions would provide a quantitative framework for CIU data analysis.
The main problem of this effort is that a mixture of Gaussian distributions could be made up of a near-infinite number of sets of peaks. Getting a good automated deconvolution method is important, but the "correct" answer will always depend on the context of the data. In the future, this package might be adapted to specifically solve ATDs. For now, however, a recommended manual step is described below.

##Installation and use.

This package can be manually installed into the python package directory. However, since there is no command line interface yet, the recommended way to use it is as a script with manual modifications to parts of the source code.
All the necessary modifications for running the package on a CIU data set are in the main() function of the Deconvolute_main module. Specific instructions are commented in the code itself. To analyse different types of data you will need to alter the functions in the parse module, but keep in mind that different data is not necessarily supported, so more modifications might be necessary.
The package also expects a specific file architecture. The data file(s) have to be in a folder parallel to the folder containing the code named 'Data' the resulting plots will be in a new folder, also parallel to the others. 

##Recommended protocol.

- Run on second derivative mode. The errors for each ATD and parameters for every Gaussian peak fitted will be printed in the form [height, mean, standard deviation].
- Chose the best fitted ATD. Copy the means of the significant peaks into the code and run again. A good cutoff for peak significance is to drop the ones that are more than two orders of magnitude less than the highest one.
- Tune the means until they fit all distributions as closely as possible. It is recomended to work with the means in index form that are printed when the program is run with the numerical means.

##Testing.

Downloading the whole repository and running Deconvolute_main will analyse Demo_data_1.txt in the Data folder. More such examples of experimental data are available in the same folder for demonstration purposes.

