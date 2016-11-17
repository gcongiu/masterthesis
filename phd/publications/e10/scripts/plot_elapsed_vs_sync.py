#!/usr/bin/python

# TODO: the script has to be made general to plot any Elapsed time starting from a csv file

# basic imports
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

    # parse command line
    (options, args) = parser.parse_args()

    # open csv data file
    datafile = pd.read_csv(options.filename)

    # index
    xlabels = ['8_4M',  '8_8M',  '8_16M',  '8_32M',  '8_64M',
               '16_4M', '16_8M', '16_16M', '16_32M', '16_64M',
               '32_4M', '32_8M', '32_16M', '32_32M', '32_64M',
               '64_4M', '64_8M', '64_16M', '64_32M', '64_64M']

    # plot the cache disable elapsed time
    matrix1 = np.transpose([datafile.shuffle_all2all[5:25], datafile.shuffle_waitall[5:25], datafile.write[5:25], datafile.post_write[5:25]])
    df1 = pd.DataFrame(matrix1,
                      index=xlabels,
                      columns=pd.Index(['shuffle_all2all','shuffle_waitall','write','post_write']))

    ax = df1.plot(kind='bar', stacked=True, alpha=0.7)
    plt.legend(loc='upper right')
    ax.set_ylabel('Elapsed [sec]')
    #ax.set_ylim(0, 23)
    plt.grid(b=None, which='major', axis='both', color='black')

    # adjust plot position
    plt.subplots_adjust(bottom=0.13)
    plt.subplots_adjust(top=0.92)
    plt.subplots_adjust(left=0.10)
    plt.subplots_adjust(right=0.95)
    plt.show()

    # plot the elapsed times for cache enable
    matrix2 = np.transpose([datafile.shuffle_all2all[30:50], datafile.shuffle_waitall[30:50], datafile.write[30:50], datafile.post_write[30:50], datafile.non_hid_sync[30:50]])
    df2 = pd.DataFrame(matrix2,
                      index=xlabels,
                      columns=pd.Index(['shuffle_alltoall','shuffle_waitall','write','post_write', 'not_hidden_sync']))

    # create two subplots sharing the x-axis
    fig, (ax, ax2) = plt.subplots(2, 1, sharex=True)

    # plot the first data frame with labels
    df2.plot(ax=ax, kind='bar', stacked=True, alpha=0.7)

    # replot the data frame without labels
    df2.plot(ax=ax2, kind='bar', stacked=True, alpha=0.7, legend=False)

    # plot ylabel and grids
    ax2.set_ylabel('Elapsed [sec]')
    plt.grid(b=None, which='major', axis='both', color='black')
    ax2.yaxis.set_label_coords(-0.05, 1.05)

    # set y limits for the two plots to cut outlayers -> requires max and min of stacked bars
    t_elapsed = datafile.shuffle_all2all[30:50]+\
                datafile.shuffle_waitall[30:50]+\
                datafile.write[30:50]+\
                datafile.post_write[30:50]
    r_elapsed = t_elapsed+\
                datafile.non_hid_sync[30:50]
    ax.set_ylim(23, 31)
    ax2.set_ylim(0, 7)


    # hide the spines between ax and ax2
    ax.spines['bottom'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    ax.xaxis.tick_top()
    ax.tick_params(labeltop='off')  # don't put tick labels at the top
    ax2.xaxis.tick_bottom()

    d = .015  # how big to make the diagonal lines in axes coordinates
    # arguments to pass plot, just so we don't keep repeating them
    kwargs = dict(transform=ax.transAxes, color='k', clip_on=False)
    ax.plot((-d, +d), (-d, +d), **kwargs)        # top-left diagonal
    ax.plot((1 - d, 1 + d), (-d, +d), **kwargs)  # top-right diagonal

    kwargs.update(transform=ax2.transAxes)  # switch to the bottom axes
    ax2.plot((-d, +d), (1 - d, 1 + d), **kwargs)  # bottom-left diagonal
    ax2.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)  # bottom-right diagonal

    # adjust plot position
    plt.subplots_adjust(bottom=0.13)
    plt.subplots_adjust(top=0.92)
    plt.subplots_adjust(left=0.10)
    plt.subplots_adjust(right=0.95)

    # print plot
    plt.show()
