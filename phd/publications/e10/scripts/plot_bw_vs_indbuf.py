#!/usr/bin/python

# TODO: the script has to be made general to plot any BW vs Indipendet buffer size starting from a csv file

# basic imports
import os
import re
import sys
import numpy as np

# import plot library and option parser
import matplotlib.pyplot as plt
import pandas as pd
from optparse import OptionParser

# for a buffer size in bytes returns the compact form
# e.g.: 4094Bytes = 4K
def reformat_buffer_size(size):
    # convert bytes into int
    num = int(size)

    # bytes multiples
    multiples = ['K','M','G']

    # initialize counter
    count = -1

    while num >= 1024:
        num /= 1024
        count += 1

    # return the new formatted string
    return str(num)+str(multiples[count])

if __name__ == "__main__":

    # check command line input
    parser = OptionParser()
    parser.add_option("-f", "--file",
                      dest="filename",
                      type="string",
                      help="file with list of csv data file names")
    parser.add_option("-s", "--size",
                      dest="filesize",
                      type="string",
                      help="size in MBs of the shared file used for the tests")

    # parse command line
    (options, args) = parser.parse_args()

    # size of the shared file used in the experiments
    filesize = int(options.filesize)

    # get the list of file names containing the cvs data to be plotted
    filelist = open(options.filename)
    files = []
    for line in filelist:
        files.append('%s'%line.strip())

    # index
    xlabels = ['4_4M_512K_0', '4_4M_1M_0', '4_4M_4M_0', '4_4M_8M_0', '4_4M_16M_0',
               '8_4M_512K_0', '8_4M_1M_0', '8_4M_4M_0', '8_4M_8M_0', '8_4M_16M_0',
               '16_4M_512K_0', '16_4M_1M_0', '16_4M_4M_0', '16_4M_8M_0', '16_4M_16M_0',
               '32_4M_512K_0', '32_4M_1M_0', '32_4M_4M_0', '32_4M_8M_0', '32_4M_16M_0',
               '64_4M_512K_0', '64_4M_1M_0', '64_4M_4M_0', '64_4M_8M_0', '64_4M_16M_0']

    ylabels = [700, 900, 1100, 1300, 1500, 1700, 1900, 2100, 2300, 2500, 2700, 2900, 3100]

    # plot markers
    markers = ['o', '^']
    labels = ['bw_cache_disable','bw_cache_enable']

    fig, ax1 = plt.subplots()
    count = 0
    lns1 = lns2 = lns3 = []
    for fil in files:
        data = pd.read_csv(fil)
        if labels[count] == 'bw_cache_disable':
            bw = filesize / (data.shuffle_write[0:25] + data.write[0:25] + data.post_write[0:25])
            bw = [bw[0],bw[0],bw[0],bw[0],bw[0],bw[5],bw[5],bw[5],bw[5],bw[5],
                  bw[10],bw[10],bw[10],bw[10],bw[10], bw[15],bw[15],bw[15],bw[15],bw[15],
                  bw[20],bw[20],bw[20],bw[20],bw[20]]
            lns1 = ax1.plot(range(len(xlabels)), bw, linestyle='-', marker=markers[count], alpha=0.7, label=labels[count])
        else:
            bw = filesize / (data.shuffle_write[0:25] + data.write[0:25] + data.post_write[0:25])
            lns2 = ax1.plot(range(len(xlabels)), bw, linestyle='-', marker=markers[count], alpha=0.7, label=labels[count])
        count += 1

    plt.yticks(ylabels)
    plt.xticks(range(len(xlabels)), xlabels, rotation='vertical')
    plt.subplots_adjust(bottom=0.22)
    ax1.set_ylabel('MB/s')
    plt.grid()

    ax2 = ax1.twinx()
    ax2.set_ylabel('seconds')
    lns3 = plt.plot(range(len(xlabels)), data.sync[0:25], linestyle='--', color='r', marker='*', alpha=0.7, label='sync')
    lns = lns1 + lns2 + lns3
    labs = [l.get_label() for l in lns]
    plt.legend(lns, labs, bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=3, mode='expand', borderaxespad=0.)
    plt.show()
