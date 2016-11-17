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
#    xlabels = ['8_4M',  '8_8M',  '8_16M',  '8_32M',  '8_64M',
#               '16_4M', '16_8M', '16_16M', '16_32M', '16_64M',
#               '32_4M', '32_8M', '32_16M', '32_32M', '32_64M',
#               '64_4M', '64_8M', '64_16M', '64_32M', '64_64M']

    xlabels = ['2_1M', '2_2M', '2_4M', '2_8M', '2_16M',
               '4_1M', '4_2M', '4_4M', '4_8M', '4_16M',
               '8_1M', '8_2M', '8_4M', '8_8M', '8_16M',
               '16_1M', '16_2M', '16_4M', '16_8M', '16_16M']

    # plot the cache disable elapsed time
    matrix1 = np.transpose([datafile.shuffle_all2all[5:25], datafile.shuffle_waitall[5:25], datafile.write[5:25], datafile.post_write[5:25]])
    df = pd.DataFrame(matrix1,
                      index=xlabels,
                      columns=pd.Index(['shuffle_all2all','shuffle_waitall','write','post_write'], name='Elapsed'))

    ax = df.plot(kind='bar', stacked=True, alpha=0.7)
    ax.set_ylabel('Elapsed [sec]')
    plt.subplots_adjust(bottom=0.25, top=0.87)
    #plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=3, mode='expand', borderaxespad=0.)
    plt.legend()
    plt.grid(b=None, which='major', axis='both', color='black')
    plt.show()

    # plot the cache enable elapsed time
    #matrix = np.transpose([datafile.shuffle_all2all, datafile.shuffle_waitall, datafile.write, datafile.post_write, datafile.sync])
    matrix2 = np.transpose([datafile.shuffle_all2all[30:50], datafile.shuffle_waitall[30:50], datafile.write[30:50], datafile.post_write[30:50], datafile.non_hid_sync[30:50]])
    df = pd.DataFrame(matrix2,
                      index=xlabels,
                      columns=pd.Index(['shuffle_all2all','shuffle_waitall','write','post_write', 'non_hidden_sync'], name='Elapsed'))

    # plot data frame
    ax = df.plot(kind='bar', stacked=True, alpha=0.7)
    ax.set_ylabel('Elapsed [sec]')
    plt.subplots_adjust(bottom=0.25, top=0.87)
    #plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=3, mode='expand', borderaxespad=0.)
    plt.legend()
    plt.grid(b=None, which='major', axis='both', color='black')
    plt.show()
#
#    xlabels = ['disable_4_4M',   'enable_4_4M',
#               'disable_4_8M',   'enable_4_8M',
#               'disable_4_16M',  'enable_4_16M',
#               'disable_4_32M',  'enable_4_32M',
#               'disable_4_64M',  'enable_4_64M',
#               'disable_8_4M',   'enable_8_4M',
#               'disable_8_8M',   'enable_8_8M',
#               'disable_8_16M',  'enable_8_16M',
#               'disable_8_32M',  'enable_8_32M',
#               'disable_8_64M',  'enable_8_64M',
#               'disable_16_4M',  'enable_16_4M',
#               'disable_16_8M',  'enable_16_8M',
#               'disable_16_16M', 'enable_16_16M',
#               'disable_16_32M', 'enable_16_32M',
#               'disable_16_64M', 'enable_16_64M',
#               'disable_32_4M',  'enable_32_4M',
#               'disable_32_8M',  'enable_32_8M',
#               'disable_32_16M', 'enable_32_16M',
#               'disable_32_32M', 'enable_32_32M',
#               'disable_32_64M', 'enable_32_64M',
#               'disable_64_4M',  'enable_64_4M',
#               'disable_64_8M',  'enable_64_8M',
#               'disable_64_16M', 'enable_64_16M',
#               'disable_64_32M', 'enable_64_32M',
#               'disable_64_64M', 'enable_64_64M']
#
#    # init transformation matrix
#    m1 = np.zeros((25,50))
#    m2 = np.zeros((25,50))
#    for i in range(0,25):
#        j = i * 2
#        m1[i][j] = 1
#        m2[i][j+1] = 1
#
#    # transform and add
#    matrix1 = np.transpose(matrix1)
#    matrix2 = np.transpose(matrix2)
#    tmp1 = np.zeros((4,50))
#    tmp2 = np.zeros((4,50))
#    for i in range(0,4):
#        for k in range(0,50):
#            for j in range(0,25):
#                tmp1[i][k] += matrix1[i][j]*m1[j][k]
#                tmp2[i][k] += matrix2[i][j]*m2[j][k]
#
#    matrix = np.transpose(tmp1 + tmp2)
#    df = pd.DataFrame(matrix,
#                      index=xlabels,
#                      columns=pd.Index(['shuffle_all2all','shuffle_waitall','write','post_write'], name='Elapsed'))
#
#    # plot data frame
#    ax = df.plot(kind='bar', stacked=True, alpha=0.7)
#    ax.set_ylabel('Elapsed [sec]')
#    plt.subplots_adjust(bottom=0.25, top=0.87)
#    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=3, mode='expand', borderaxespad=0.)
#    plt.grid(b=None, which='major', axis='both', color='black')
#    plt.show()
#
