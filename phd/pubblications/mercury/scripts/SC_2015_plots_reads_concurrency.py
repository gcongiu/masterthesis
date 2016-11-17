#!/usr/bin/env python

__author__ = 'padua'


import os
import argparse
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
#import seaborn
#plt.style.use('ggplot')
#plt.style.use('dark_background')
#print plt.style.available
plt.rc('text', color='black')
plt.rc('axes.formatter', use_mathtext=True)
plt.rc('legend', numpoints=1)
#ext4 = True   # it holds for GPFS too

KB = 1024
MB = KB * 1024
GB = MB * 1024
TB = GB * 1024


def argparse_of_program():
    parser = argparse.ArgumentParser(description='This script generates box plots for I/O server reads')

    parser.add_argument('-d', '--dir', help='Input directory where all results are', required=True)
    parser.add_argument('-m', '--mogon', help='mogon or not', required=True)
    args = parser.parse_args()
    return args


def get_cwd():
    return os.getcwd()


def get_list_of_filesdirindir(dir):
    return os.listdir(dir)


def evaluate_mean(list_of_values):
    return np.mean(1.0 * np.array(list_of_values))


def evaluate_std(list_of_values):
    return np.std(1.0 * np.array(list_of_values))


def read_runtime(path_file):
    with open(path_file, 'r') as f:
        findings = json.load(f)
        runtime = findings["runtime"]
        return runtime


def read_reads_info(path_file):
    with open(path_file, 'r') as f:
        findings = json.load(f)
        server_reads = findings["reads"]
        return server_reads


def read_read_bytes(path_file):
    with open(path_file, 'r') as f:
        findings = json.load(f)
        server_reads = findings["read bytes"]
        return server_reads

#### client info
def read_reads_client_info(path_file):
    with open(path_file, 'r') as f:
        findings = json.load(f)
        client_reads = findings["reads_client"]
        return client_reads


def read_read_bytes_client(path_file):
    with open(path_file, 'r') as f:
        findings = json.load(f)
        client_reads = findings["read_bytes_client"]
        return client_reads


def name_input_files(labell):
    if '5GB' in labell and len(labell) == 3:
        filename = '00050'
    else:
        files = str(int(labell[:-2])/5)
        filename = 'huge_new_file_%ssources' % files
    return filename


def create_sorted_list_procs(directoryname):
    set_of_simultan_procs = set()
    direct = os.path.join(get_cwd(), directoryname)
    for dire in os.listdir(direct):
        dirr = os.path.join(direct, dire)
        true_false_flag = dirr.split("/")[len(dirr.split("/"))-1].split("_")[1].split("-")[1]  # True or False
        for fil in os.listdir(dirr):
            if "result" in fil.split(".")[0]:
                file_path = os.path.join(dirr, fil)

                with open(file_path, 'r') as fi:
                    dict_with_results = json.load(fi)
                    if 'y' in arg_of_program.mogon:
                        simult_procs = int(file_path.split("/")[len(file_path.split("/"))-1].split(".")[3])
                    else:
                        simult_procs = int(file_path.split("/")[len(file_path.split("/"))-1].split(".")[2])
                    set_of_simultan_procs.add(simult_procs)
    list_procs = sorted(set_of_simultan_procs)
    return list_procs




if __name__ == '__main__':

    arg_of_program = argparse_of_program()   #get the parameters (dir with results)
    list_proc_sim = create_sorted_list_procs(arg_of_program.dir)
    max_procs_simult = int(list_proc_sim[len(list_proc_sim)-1])

    list_true = [[] for j in range(len(list_proc_sim))]
    list_false = [[] for j in range(len(list_proc_sim))]

    root_result_dir = arg_of_program.dir
    direct = os.path.join(get_cwd(), root_result_dir)
    for dire in os.listdir(direct):
        dirr = os.path.join(direct, dire)
        true_false_flag = dirr.split("/")[len(dirr.split("/"))-1].split("_")[1].split("-")[1]  # True or False
        for fil in os.listdir(dirr):
            if "result" in fil.split(".")[0]:
                file_path = os.path.join(dirr, fil)

                with open(file_path, 'r') as fi:
                    dict_with_results = json.load(fi)
                    if 'y' in arg_of_program.mogon:
                        simult_procs = int(file_path.split("/")[len(file_path.split("/"))-1].split(".")[3])
                    else:
                        simult_procs = int(file_path.split("/")[len(file_path.split("/"))-1].split(".")[2])

                for j in list_proc_sim:
                    if simult_procs == int(j):
                        #print(file_path)
                        #print(max_procs)
                        if "True" in true_false_flag:

                            list_true[list_proc_sim.index(j)].append(dict_with_results["disk_stats"]["reads"])
                        elif "False" in true_false_flag:

                            list_false[list_proc_sim.index(j)].append(dict_with_results["disk_stats"]["reads"])


    groups = []
    for u in range(len(list_true)):
        groups.append(list_false[u])
        groups.append(list_true[u])

    #print(groups)

    maxima_false = []
    minima_false = []
    average_false = []

    maxima_true = []
    minima_true = []
    average_true = []


    #print(list_false)

    for u in range(len(list_true)):
        maxima_false.append(np.max(list_false[u]))
        maxima_true.append(np.max(list_true[u]))

        minima_false.append(np.min(list_false[u]))
        minima_true.append(np.min(list_true[u]))

        average_false.append(np.mean(list_false[u]))
        average_true.append(np.mean(list_true[u]))


    #print(maxima_false)
    #print(maxima_true)
    #print(len(maxima_false))
    #print(len(maxima_true))

    # Create a figure instance
    fig = plt.figure(1, figsize=(9, 6))
    #fig = plt.figure(figsize=(6, 4))

    # Create an axes instance
    ax = fig.add_subplot(111)


    lo = 2
    lu = 1

    pos = []
    for i in range(len(list_proc_sim)):
        low = lo
        high = low+1
        pos.append(low)
        pos.append(high)
        lo += 3


    pos_false = []
    pos_true = []
    for j in range(0, len(pos), 2):
        pos_false.append(pos[j])

    for j in range(1, len(pos), 2):
        pos_true.append(pos[j])

    plt.plot(pos_false, minima_false, marker='x', markersize=3, linestyle='none', color='black')
    plt.plot(pos_false, maxima_false, marker='x', markersize=3, linestyle='none', color='black')
    plt.plot(pos_false, average_false, marker='x', markersize=3, linestyle='--', color='black', label='w/o SAIO')

    plt.plot(pos_true, minima_true, marker='*', markersize=3, linestyle='none', color='black')
    plt.plot(pos_true, maxima_true, marker='*', markersize=3, linestyle='none', color='black')
    plt.plot(pos_true, average_true, marker='*', markersize=3, linestyle='-', color='black', label='w/ SAIO')

    #plt.plot(pos_false, average_false, linestyle='--', color='black')
    #plt.plot(pos_true, average_true, linestyle='_', color='black')

#     #bp = ax.boxplot(groups, positions=[2, 3, 5, 6, 8, 9, 11, 12, 14,15, 17,18, 20,21, 23,24, 26, 27, 29,30, 32,33, 35,36], widths=0.6)
#     #whiskerprops = dict(linestyle='')
#     capprops = dict(marker='*', markerfacecolor='black', markersize=4, color='black')
#     meanpointprops = dict(marker='x', markeredgecolor='black', markerfacecolor='black')
#     #medianprops = dict(marker='D', markeredgecolor='black', markerfacecolor='black', linestyle='none')
#     bp = ax.boxplot(groups, positions=pos, widths=0.6, whis='range', showbox=False, showcaps=True, showmeans=True, meanprops=meanpointprops, capprops=capprops)  # , medianprops=medianprops)
#     #plt.setp(bp['boxes'], color='black')
#     #plt.setp(bp['whiskers'], color='black')
#     #plt.setp(bp['fliers'], color='black', marker='+')
#
#     ## change color and linewidth of the whiskers
#     for whisker in bp['whiskers']:
#         whisker.set(color='white')
#     median = []
#     for medline in bp['medians']:
#         linedata = medline.get_ydata()
#         median.append(linedata[0])
#     plt.scatter(pos, median)
#
#     for cap in bp['caps']:
#     #    cap.set(color='black', linestyle=None, marker='*')
#         print(cap.get_xdata())
#         print(cap.get_ydata())
#         print(len(cap.get_xdata()))
#         print(len(cap.get_ydata()))
# ## change color and linewidth of the caps
#     #for cap in bp['caps']:
#     #    cap.set(color='black', linestyle=None, marker='*')
#
# ## change color and linewidth of the medians
#     #for median in bp['medians']:
#     #    median.set(color='#b2df8a', linewidth=2)
#
# ## change the style of fliers and their fill
#     #for flier in bp['fliers']:
#     #    flier.set(marker='o', color='#e7298a', alpha=0.5)
#
#
#
#
#     # Now fill the boxes with desired colors
#     #boxColors = ['darkkhaki', 'royalblue']
#     #boxColors = ['0.2', '0.8']
#      # Now fill the boxes with desired colors
#     boxColors = ['0.9', 'orangered']
#     #boxColors = ['darkkhaki', 'royalblue']
#     #boxColors = ['0.2', '0.8']
#     numBoxes = len(list_proc_sim)*2
#     medians = range(numBoxes)
#
#     """
#     for i in range(numBoxes):
#         box = bp['boxes'][i]
#         med = bp['medians'][i]
#         boxX = []
#         boxY = []
#         for j in range(5):
#             boxX.append(box.get_xdata()[j])
#             boxY.append(box.get_ydata()[j])
#         boxCoords = zip(boxX, boxY)
#       # Alternate between Dark Khaki and Royal Blue
#         k = i % 2
#         boxPolygon = Polygon(boxCoords, facecolor=boxColors[k])
#         ax.add_patch(boxPolygon)
#
#         plt.plot([np.average(med.get_xdata())], [np.average(groups[i])],
#            color='black', marker='*', markeredgecolor='k')
#     """
#

    #print numBoxes
    xlabels = []
    xticks = []
    x_l = 2.5
    for i in range(len(list_proc_sim)):
        xlabels.append(list_proc_sim[i])
        xticks.append(x_l)
        x_l += 3
    xlim = [0, pos[len(list_proc_sim)*2-1]+1]
    #print(pos[len(list_proc_sim)*2-1])
    #print(xticks[len(list_proc_sim)-1])
    ax.set_xticklabels(xlabels, fontsize=13)

    ax.set_xlim(xlim)
    ax.set_xticks(xticks)


    #without_patch = mpatches.Patch(color='0.9', label='w/o SAIO')
    #with_patch = mpatches.Patch(color='orangered', label='w/ SAIO')
    #star = mlines.Line2D([], [], color='black', marker='*', label='average', linestyle='None')
    if 'gpfs' in root_result_dir:
        title_legend = 'GPFS'
    #plt.legend(loc='upper left', handles=[without_patch, with_patch, star], title='GPFS', fancybox=True, fontsize=13)
        #plt.legend(loc='upper left', handles=[without_patch, with_patch, star], title='GPFS', fancybox=True, fontsize=13)
    elif 'ext4' in root_result_dir:
        title_legend = 'ext4'
    elif 'Lustre' in root_result_dir:
        title_legend = 'Lustre'

    plt.setp(ax.yaxis.get_majorticklabels(), fontsize=13)

    l = plt.legend(loc='upper left', title=title_legend, fancybox=True, fontsize=14)
    plt.setp(l.get_title(), fontsize=15)  # trick to set legend title font size

    plt.xlabel('# simultaneous app instances', fontsize=18)
    plt.ylabel('server reads', fontsize=18)

    plt.tight_layout()
    plt.show()