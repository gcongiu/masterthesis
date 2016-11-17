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
    bw = filesize / (datafile.shuffle_write + datafile.write + datafile.post_write)

    # index
    xlabels = ['4_4M',  '4_8M',  '4_16M',  '4_32M',  '4_64M',
               '8_4M',  '8_8M',  '8_16M',  '8_32M',  '8_64M',
               '16_4M', '16_8M', '16_16M', '16_32M', '16_64M',
               '32_4M', '32_8M', '32_16M', '32_32M', '32_64M',
               '64_4M', '64_8M', '64_16M', '64_32M', '64_64M']

    ylabels = [500, 700, 900, 1100, 1300, 1500, 1700, 1900, 2100, 2300, 2500, 2700, 2900]

    # create plot cache disable
    fig, ax1 = plt.subplots()
    x = np.arange(0, 25, 1)

    # add bandwidth subplots
    lns1 = ax1.plot(x, bw[0:25], linestyle='-', color='g', marker='x', alpha=0.7, label='Write Bandwidth')
    ax1.set_ylabel('MB/s')

    # increase the number of points along y-axis
    plt.yticks(ylabels)

    # updated xticks with experiments configuration
    plt.xticks(range(len(xlabels)), xlabels, rotation='vertical')
    plt.subplots_adjust(bottom=0.25)

    # add gridlines
    plt.grid(b=None, which='major', axis='both', color='black')

    # disconnect the second axis from the first
    ax2 = ax1.twinx()

    # add standard deviation subplot
    stdperc = datafile.write_std[0:25]/(datafile.shuffle_write[0:25]+datafile.write[0:25]+datafile.post_write[0:25])*100
    lns2 = ax2.plot(x, stdperc, linestyle='--', color='r', marker='o', alpha=0.7, label='Write Time Standard Deviation')
    ax2.set_ylabel('io time %')

    # add legend
    lns = lns1 + lns2
    labs = [l.get_label() for l in lns]
    plt.legend(lns, labs, bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode='expand', borderaxespad=0.)

    # show plot
    plt.show()

    #ylabels = [1000, 3000, 5000, 7000, 9000, 11000, 13000, 15000, 17000, 19000, 21000, 23000, 25000, 27000, 29000, 31000, 33000, 35000] #, 37000, 39000, 41000, 43000, 45000]
    ylabels = [500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500]

    # create plot cache enable
    fig, ax1 = plt.subplots()
    x = np.arange(0, 25, 1)
    lns1 = ax1.plot(x, bw[25:50], linestyle='-', color='g', marker='x', alpha=0.7, label='Write Bandwidth')
    ax1.set_ylabel('MB/s')
    plt.yticks(ylabels)
    plt.xticks(range(len(xlabels)), xlabels, rotation='vertical')
    plt.subplots_adjust(bottom=0.25)
    plt.grid(b=None, which='major', axis='both', color='black')

    ax2 = ax1.twinx()
    stdperc = datafile.write_std[25:50]/(datafile.shuffle_write[25:50]+datafile.write[25:50]+datafile.post_write[25:50])*100
    lns2 = ax2.plot(x, stdperc, linestyle='--', color='r', marker='o', alpha=0.7, label='Write Time Standard Deviation')
    ax2.set_ylabel('io time %')
    lns = lns1 + lns2
    labs = [l.get_label() for l in lns]
    plt.legend(lns, labs, bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode='expand', borderaxespad=0.)
    plt.show()
