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

    # shift width
    width = 0.5

    # create xrange points
    x = np.arange(0, 40, 2)

    # index
    xlabels = ['8_4M',  '8_8M',  '8_16M',  '8_32M',  '8_64M',
               '16_4M', '16_8M', '16_16M', '16_32M', '16_64M',
               '32_4M', '32_8M', '32_16M', '32_32M', '32_64M',
               '64_4M', '64_8M', '64_16M', '64_32M', '64_64M']

    # plot the cache disable elapsed time
    shuffle_alltoall = datafile.shuffle_all2all[5:25]
    shuffle_waitall  = datafile.shuffle_waitall[5:25]
    write            = datafile.write[5:25]
    post_write       = datafile.post_write[5:25]
    non_hid_sync     = datafile.non_hid_sync[5:25]

    # create plots for cache enable and disable
    fig, ax1 = plt.subplots()
    lns1 = ax1.bar(x-0.5*width, shuffle_alltoall, width, color='r', label='shuffle_alltoall')
    lns2 = ax1.bar(x-0.5*width, shuffle_waitall, width, color='g', label='shuffle_waitall')
    lns3 = ax1.bar(x-0.5*width, write, width, color='b', label='write')
    lns4 = ax1.bar(x-0.5*width, non_hid_sync, width, color='y', label='non_hiddend_sync')

    plt.show()

