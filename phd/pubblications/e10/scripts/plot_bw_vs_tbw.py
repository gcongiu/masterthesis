#!/usr/bin/python

# TODO: the script has to be made general to plot any BW vs Std starting from a csv file

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
                      help="csv data file name")
    parser.add_option("-s", "--size",
                      dest="filesize",
                      type="string",
                      help="size in MBs of the shared file used for the tests")

    # parse command line
    (options, args) = parser.parse_args()

    # open csv data file
    datafile = pd.read_csv(options.filename)

    # size of the shared file used in the experiments
    filesize = int(options.filesize)

    # compute bandwidth vector
    bw = filesize / (datafile.tot + datafile.non_hid_sync)
    tbw = filesize / datafile.tot

    # shift width
    width = 0.5

    # create plot cache disable
    x = np.arange(0, 40, 2)

    # create plots for cache disable and enable
    fig, ax1 = plt.subplots()
    lns1 = ax1.bar(x-1.5*width, bw[5:25], width, color='r', label='BW Cache Disable', edgecolor='black', log='true')
    lns2 = ax1.bar(x-0.5*width, bw[30:50], width, color='g', label='BW Cache Enable', edgecolor='black', log='true')
    lns3 = ax1.bar(x+0.5*width, tbw[30:50], width, color='b', label='TBW Cache Enable', edgecolor='black', log='true')

    # add yticks for logarithmic scale
    #ylabels = [10, 100, 1000, 1000, 10000, 100000]
    ylabels = [1, 10, 100, 1000, 10000]
    ax1.set_yticks(ylabels)

    # add xticks for experiments
#    xlabels = ['2_1M', '', '2_2M', '', '2_4M', '', '2_8M', '', '2_16M', '',
#               '4_1M', '', '4_2M', '', '4_4M', '', '4_8M', '', '4_16M', '',
#               '8_1M', '', '8_2M', '', '8_4M', '', '8_8M', '', '8_16M', '',
#               '16_1M','', '16_2M','', '16_4M','', '16_8M','', '16_16M', '']

    xlabels = ['8_4M',  '', '8_8M',  '', '8_16M',  '', '8_32M',  '', '8_64M',  '',
               '16_4M', '', '16_8M', '', '16_16M', '', '16_32M', '', '16_64M', '',
               '32_4M', '', '32_8M', '', '32_16M', '', '32_32M', '', '32_64M', '',
               '64_4M', '', '64_8M', '', '64_16M', '', '64_32M', '', '64_64M', '']

    plt.xticks(range(len(xlabels)), xlabels, rotation='vertical')

    # plot ylabel
    plt.ylabel('MB/s')

    # draw plot grid
    plt.grid(True)

    # plot legend
    plt.legend(loc=2)

    # add title
    plt.xlim([-1.5, len(xlabels)-0.5])
    #plt.title('Write Bandwidth')

    # adjust plot position
    plt.subplots_adjust(bottom=0.13)
    plt.subplots_adjust(top=0.92)
    plt.subplots_adjust(left=0.10)
    plt.subplots_adjust(right=0.95)
    plt.show()
