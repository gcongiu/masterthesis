#!/usr/bin/python

# TODO: the script has to be made general to plot any BW vs Delay starting from a csv file

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
    xlabels = ['4_4M_512K', '4_8M_512K', '4_16M_512K', '4_32M_512K', '4_64M_512K',
               '8_4M_512K', '8_8M_512K', '8_16M_512K', '8_32M_512K', '8_64M_512K',
               '16_4M_512K', '16_8M_512K', '16_16M_512K', '16_32M_512K', '16_64M_512K',
               '32_4M_512K', '32_8M_512K', '32_16M_512K', '32_32M_512K', '32_64M_512K',
               '64_4M_512K', '64_8M_512K', '64_16M_512K', '64_32M_512K', '64_64M_512K']

    ylabels = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000, 14000, 15000, 16000, 17000]

    # plot markers
    markers = ['+', 'x', 'o', '*', '^']
    labels = ['base', 'delay_0', 'delay_0.5', 'delay_1', 'delay_1.5']

    fig, ax1 = plt.subplots()
    count = 0
    for fil in files:
        data = pd.read_csv(fil)
        if count == 0: # this case we add the sync time to the bandwidth
            bw = filesize / (data.shuffle_write[0:25] + data.write[0:25] + data.post_write[0:25])
            ax1.plot(range(len(xlabels)), bw, linestyle='--', marker=markers[count], alpha=0.7, label=labels[count])
            count += 1
            bw = filesize / (data.shuffle_write[25:50] + data.write[25:50] + data.post_write[25:50] + data.sync[25:50])
            ax1.plot(range(len(xlabels)), bw, linestyle='-', marker=markers[count], alpha=0.7, label=labels[count])
            count += 1
        else: # sync is not overlapped with computation and thus we don't need to add it
            bw = filesize / (data.shuffle_write[25:50] + data.write[25:50] + data.post_write[25:50])
            ax1.plot(range(len(xlabels)), bw, linestyle='-', marker=markers[count], alpha=0.7, label=labels[count])
            count += 1

    plt.yticks(ylabels)
    plt.xticks(range(len(xlabels)), xlabels, rotation='vertical')
    plt.subplots_adjust(bottom=0.2, top=0.85)
    ax1.set_ylabel('MB/s')
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=3, mode='expand', borderaxespad=0.)
    plt.grid()
    plt.show()

    fig, ax1 = plt.subplots()
    count = 0
    for fil in files:
        data = pd.read_csv(fil)
        if count == 0:
            ax1.plot(range(len(xlabels)), data.write[0:25], linestyle='--', marker=markers[count], alpha=0.7, label=labels[count])
            count += 1
            ax1.plot(range(len(xlabels)), data.sync[25:50], linestyle='-', marker=markers[count], alpha=0.7, label=labels[count])
            count += 1
        else:
            ax1.plot(range(len(xlabels)), data.sync[25:50], linestyle='-', marker=markers[count], alpha=0.7, label=labels[count])
            count += 1

    plt.xticks(range(len(xlabels)), xlabels, rotation='vertical')
    plt.subplots_adjust(bottom=0.2, top=0.85)
    ax1.set_ylabel('seconds')
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=3, mode='expand', borderaxespad=0.)
    plt.grid()
    plt.show()
