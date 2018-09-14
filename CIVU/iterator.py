"""Iterates over directory with data. Requires very specific architecture and 
the map file.


Created by Simos Kalfas
    email:simos.kalfas@gmail.com
    github: https://github.com/simoskalfas/
"""

import Deconvolute_main
import time


def smooth_iterator():
	"""Iterator function.

	This function was made to parse and analyse a specific data set. It is not
	recomended to use. If it is required, a file in the style of 
	Cyclic_means_full.tsv will need to be present in the same directory as the 
	package directory. An example is provided. The parsing will have to be 
	altered to produce appropriate titles.

	Args:
		None.

	Returns:
		Nothing.
	"""
	with open('../Cyclic_means_full.tsv', 'r') as f:
		means = {}
		for line in f:
			l = line.replace('\n', '')
			l = l.replace('[', '')
			l = l.replace(']', '')
			l = l.replace(' ', '')
			l = l.split('\t')
			l[1] = l[1].split(',')
			l[2] = l[2].split('.')
			l[2] = [int(i) for i in l[2]]
			l[1] = [int(i) for i in l[1]]
			means[l[0]] = [l[1], l[2]]
	smooth = [3, 2]
	res_filename = '_3_2_erind'
	for key in means:
		print key
		filename = 'adc_' + key
		title = key[::]
		title = title.replace('_combined', '')
		title = title.replace('_', ' ')
		title = title.replace('blac', r'$\beta$' + 'Lac')
		title = title.replace('cytc', 'CytC')
		title = title.replace('cona', 'ConA')
		title = title.replace('amac', 'AmAc buffer')
		title = title.replace('wma', 'WMA buffer')
		title = title.replace('trapBIAS', 'CIU')
		title = title.replace('trapCE', 'CIU')
		for i in range(len(title) - 1):
			if title[i].isdigit() and not title[i+1].isdigit():
				title = title[:i] + '+' + title[i:]
				break
		ciu=False
		aline=True
		if 'CIU' in title:
			ciu=True
			aline=False
		Deconvolute_main.deconvolve(filename, res_filename, smooth, 
			means[key][0], title, means[key][1], ciu=ciu, cycles=5, aline=aline)


def main():
	start_time = time.time()
	smooth_iterator()
	print time.time() - start_time
	print 'full time elapsed'
	return



if __name__ == '__main__':
    main()