"""Module containing parsing and alining functions.


Created by Simos Kalfas
    email:simos.kalfas@gmail.com
    github: https://github.com/simoskalfas/
"""
from scipy.signal import  argrelmax
import numpy as np


# def handle_file(filename):
#     datdic = {}
#     with open('../Data/' + filename + '.txt', 'r') as f:
#         datdic[filename] = []
#         datdic['data'] = []
#         f.readline()
#         for line in f:
#             spl = line.replace('\r', '')
#             spl = spl.replace('\n', '')
#             spl = spl.split('\t')
#             datdic[filename].append(float(spl[0]))
#             datdic['data'].append(float(spl[1]))
#     return datdic

def handle_file(filename, make_txt=False):
    """Parses the data file into a dictionary.

    Args:
        filename:Data file name without file extension
        make_txt:If True, outputs a text file with the parsed data

    Returns:
        datadic:Dictionary of data 
            {filename:arrival times, voltage1:intensities1, ...}
    """
    datdic = {}
    with open('../Data/' + filename + '.txt', 'r') as f:
        fl = f.readline()
        fl = fl.replace('\r', '')
        fl = fl.replace('\n', '')
        fl = fl.split('\t')
        fl[0] = filename
        for i in range(len(fl)):
            datdic[str(fl[i])] = []
        for line in f:
            spl = line.replace('\r', '')
            spl = spl.replace('\n', '')
            spl = spl.split('\t')
            for j in range(len(spl)):
                datdic[fl[j]].append(float(spl[j]))
    if make_txt:
        with open('splitdata.txt', 'w') as f:
            for i in datdic:
                f.write(str(i))
                f.write(str(datdic[str(i)]))
                f.write('\n')
    return datdic


def aline(datdic, filename, gen_text=False):
    """Alines data using the global maximum of each set.

    Do not use for CIU data. Only usefull for data with small folding evolution.

    Args:
        datdic: Dictionary of parsed data
        filename: Name of data file without file extension
        gen_text: If True, outputs a text file with alined data

    Returns:
        retdic: Dictionary of alined data
    """
    fullkeys = sorted(datdic)
    keys = fullkeys[:-1]
    datamat = [datdic[i] for i in keys] #Make data into matrix
    fullind = []
    for i in range(0, len(datamat)):
        alist = datamat[i][::]
        alist.sort()
        peaks = alist[-2:] #Get maximum
        #If the maximum conformation changes, uncomment line 68 and comment line
        #69
        #alind = argrelmax(np.array(datamat[i]), order=5)[0][:2]
        alind = [datamat[i].index(j) for j in peaks]
        alind.sort()
        fullind.append(alind)
    firstind = [i[0] for i in fullind]
    disp = [i - min(firstind) for i in firstind] #Displacement factor
    print 'Alinement displacement:' + str(disp) 
    for i in range(0, len(datamat)): #Aline data
        datamat[i] = datamat[i][disp[i]:]
        datamat[i] += [0 for _ in range(disp[i])]
    retdic = {}
    for i in range(len(keys)):
        retdic[keys[i]] = datamat[i]
    retdic[fullkeys[-1]] = datdic[fullkeys[-1]]
    if gen_text:
        with open(filename + 'alined_' + '.txt', 'w') as f:
            for i in sorted(retdic):
                f.write(str(i))
                f.write('\t')
            f.write('\n')
            for i in range(len(retdic[keys[0]])):
                for j in sorted(retdic):
                    f.write(str(retdic[j][i]))
                    f.write('\t')
                f.write('\n')
    return retdic


def main():
    return


if __name__ == '__main__':
    main()
