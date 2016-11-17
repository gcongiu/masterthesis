#!/usr/bin/env python

__author__ = 'padua'


import os
import argparse
import json
import numpy as np
import matplotlib.pyplot as plt
#import prettyplotlib
#import seaborn as sns

#plt.rc('text', usetex=True)
plt.rc('text', color='black')
plt.rc('axes.formatter', use_mathtext=True)


KB = 1024
MB = KB * 1024
GB = MB * 1024
TB = GB * 1024


def plot_line_points(x, y1, y2, y1_err, y2_err, xlabel, lab_coord_true, lab_coord_false, ylabel):

    plt.figure(figsize=(xlabel.__len__(), 11))
    plt.xticks(x, xlabel)
    plt.yticks(fontsize=20)
    #plt.title('# Operations per month', fontsize=30)
    #plt.xlabel('Months', fontsize=20)
    plt.ylabel(ylabel, fontsize=20)
    plt.grid(True)

    plt.errorbar(x, y1, y1_err, color='0', label=lab_coord_true, marker='o', linestyle='-', linewidth=2)
    plt.errorbar(x, y2, y2_err, color='0', label=lab_coord_false, marker='s', linestyle='--', linewidth=2)

    plt.legend(loc='upper left', fontsize=20)
    #plt.subplots_adjust(top=.91)
    #plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
    plt.tight_layout()
    #plt.show()



def plot_line_points_percentage(x, y1, y2, y1_err, y2_err, xlabel, lab_coord_true, lab_coord_false, ylabel):
    plt.figure(figsize=(10, 5))
    plt.xticks(x, xlabel)
    plt.yticks(fontsize=14)
    #plt.title('# Operations per month', fontsize=30)
    #plt.xlabel('Months', fontsize=20)
    plt.ylabel(ylabel, fontsize=18)
    plt.grid(True)
    y = ((y1 - y2)/y2) * 100

    plt.plot(x, y, marker='o', linestyle='-', linewidth=2)
    #plt.errorbar(x, y1, y1_err, color='0', label=lab_coord_true, marker='o', linestyle='-', linewidth=2)
    #plt.errorbar(x, y2, y2_err, color='0', label=lab_coord_false, marker='s', linestyle='--', linewidth=2)

    #plt.legend(loc='upper left', fontsize=20)
    #plt.subplots_adjust(top=.91)
    #plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
    plt.tight_layout()
    #plt.show()


def barplot_seaborn_difference(x, y1, y2, y1_err, y2_err, xlabel, lab_coord_true, lab_coord_false, ylabel):

    #plt.figure(figsize=(xlabel.__len__(), 11))
    #plt.figure(figsize=(4, 5))

    fig = plt.figure(figsize=(xlabel.__len__(), 11), facecolor='white')
    ax = fig.add_subplot(111)

    plt.xticks(x, xlabel)
    # define y axis ticks

    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.tick_params(axis='both', direction='out')
    ax.get_xaxis().tick_bottom()   # remove unneeded ticks
    ax.get_yaxis().tick_left()
    ######## comment the above 5 lines if yo want top and right axis....
    plt.ylabel(ylabel, fontsize=21)

    y = ((y1 - y2)/ y2) * 100
    width = 0.28
    ax.bar(x, y, width)
    #plt.errorbar(x, y2, y2_err, color='0', label=lab_coord_false, marker='s', linestyle='--', linewidth=2)

    #plt.legend(loc='upper right', fontsize=20)
    #plt.subplots_adjust(top=.91)
    #plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
    plt.tight_layout()
    #plt.show()



def plot_line_points_percentage_all_metrics(x, y1, y2, y_throu_true, y_throu_false, y_reads_true, y_reads_false, y1_err, y2_err, xlabel, ylabel, legend_tile):
    #fig = plt.figure(figsize=(7, 5))
    fig = plt.figure(figsize=(6, 4))
    #fig, ax = plt.subplots(nrows=1, ncols=3, sharex=True, sharey=True)
    ax = fig.add_subplot(111)
    plt.xticks(x, xlabel, fontsize=12)
    plt.yticks(fontsize=14)
    #plt.title('# Operations per month', fontsize=30)
    plt.xlabel('File size [GB]', fontsize=16)
    plt.ylabel(ylabel, fontsize=16)
    #plt.grid(True)
    #ax.spines["right"].set_visible(False)
    #ax.spines["top"].set_visible(False)
    #ax.tick_params(axis='both', direction='out')
    y_runtime = ((y1 - y2)/y2) * 100
    y_reads = ((y_reads_true - y_reads_false)/y_reads_false) * 100
    y_thr = ((y_throu_true - y_throu_false)/y_throu_false) * 100

    y_base = []
    for i in range(0, len(y1)):
        y_base.append(0)
    y_baseline = np.array(y_base)

    ax.plot(x, y_runtime, marker='*', linestyle=':', linewidth=1, color='black', label='runtime')
    #ax = fig.add_subplot(111)
    ax.plot(x, y_reads, marker='<', linestyle='-.', linewidth=1, color='black', label='reads')
    #ax = fig.add_subplot(111)
    ax.plot(x, y_thr, marker='D', linestyle='--', linewidth=1, color='black', label='throughput')
    #ax = fig.add_subplot(111)
    ax.plot(x, y_baseline, marker='s', linestyle='-', linewidth=1, color='red', label='baseline NO AM')
    #plt.errorbar(x, y1, y1_err, color='0', label=lab_coord_true, marker='o', linestyle='-', linewidth=2)
    #plt.errorbar(x, y2, y2_err, color='0', label=lab_coord_false, marker='s', linestyle='--', linewidth=2)

    if 'GPFS prefetch enabled' in legend_tile:
        ax.axvline(x=3.2, linestyle='-', linewidth=2, color='blue')
        ax.annotate("16 GB, physical RAM",
            xy=(3.2, 11), xycoords='data',
            xytext=(5.2, 11), textcoords='data',
            size=10, va="center", ha="left",
            arrowprops=dict(arrowstyle="simple"))
    if 'Lustre new ADV Manager' in legend_tile:
        ax.axvline(x=3.2, linestyle='-', linewidth=2, color='blue')
        ax.annotate("16 GB, physical RAM",
            xy=(3.2, 50), xycoords='data',
            xytext=(5.2, 50), textcoords='data',
            size=10, va="center", ha="left",
            arrowprops=dict(arrowstyle="simple"))
    if 'GPFS new ADV Manager WRONG' in legend_tile:
        ax.axvline(x=3.2, linestyle='-', linewidth=2, color='blue')
        ax.annotate("16 GB, physical RAM",
            xy=(3.2, 11), xycoords='data',
            xytext=(5.2, 11), textcoords='data',
            size=10, va="center", ha="left",
            arrowprops=dict(arrowstyle="simple"))
    if 'GPFS new ADV Manager FIXED' in legend_tile:
        ax.axvline(x=3.2, linestyle='-', linewidth=2, color='blue')
        ax.annotate("16 GB, physical RAM",
            xy=(3.2, 11), xycoords='data',
            xytext=(5.2, 11), textcoords='data',
            size=10, va="center", ha="left",
            arrowprops=dict(arrowstyle="simple"))
    elif 'GPFS replay Tim old' in legend_tile:
        print(legend_tile)
        ax.axvline(x=3.2, linestyle='-', linewidth=2, color='blue')
        ax.annotate("16 GB, physical RAM",
            xy=(3.2, 11), xycoords='data',
            xytext=(5.2, 11), textcoords='data',
            size=10, va="center", ha="left",
            arrowprops=dict(arrowstyle="simple"))
    elif 'GPFS replay prefetch0' in legend_tile:
        print(legend_tile)
        ax.axvline(x=3.2, linestyle='-', linewidth=2, color='blue')
        ax.annotate("16 GB, physical RAM",
            xy=(3.2, 500), xycoords='data',
            xytext=(5.2, 500), textcoords='data',
            #xy=(0, 0), xycoords='data',
            #xytext=(0, 0), textcoords='data',
            size=10, va="center", ha="left",
            arrowprops=dict(arrowstyle="simple"))
    elif 'GPFS replay prefetch1' in legend_tile:
        print(legend_tile)
        ax.axvline(x=3.2, linestyle='-', linewidth=2, color='blue')
        ax.annotate("16 GB, physical RAM",
            xy=(3.2, 11), xycoords='data',
            xytext=(5.2, 11), textcoords='data',
            size=10, va="center", ha="left",
            arrowprops=dict(arrowstyle="simple"))
    elif 'GPFS replay prefetch2' in legend_tile:
        print(legend_tile)
        ax.axvline(x=3.2, linestyle='-', linewidth=2, color='blue')
        ax.annotate("16 GB, physical RAM",
            xy=(3.2, 11), xycoords='data',
            xytext=(5.2, 11), textcoords='data',
            size=10, va="center", ha="left",
            arrowprops=dict(arrowstyle="simple"))
    elif 'GPFS replay prefetch3' in legend_tile:
        print(legend_tile)
        ax.axvline(x=3.2, linestyle='-', linewidth=2, color='blue')
        ax.annotate("16 GB, physical RAM",
            xy=(3.2, 11), xycoords='data',
            xytext=(5.2, 11), textcoords='data',
            size=10, va="center", ha="left",
            arrowprops=dict(arrowstyle="simple"))
    elif 'GPFS replay prefetch4' in legend_tile:
        print(legend_tile)
        ax.axvline(x=3.2, linestyle='-', linewidth=2, color='blue')
        ax.annotate("16 GB, physical RAM",
            xy=(3.2, 11), xycoords='data',
            xytext=(5.2, 11), textcoords='data',
            size=10, va="center", ha="left",
            arrowprops=dict(arrowstyle="simple"))
    elif 'GPFS prefetch disabled' in legend_tile:
        ax.axvline(x=3.2, linestyle='-', linewidth=2, color='blue')
        ax.annotate("16 GB, physical RAM",
            xy=(3.2, 205), xycoords='data',
            xytext=(5.2, 205), textcoords='data',
            size=10, va="center", ha="left",
            arrowprops=dict(arrowstyle="simple"))
    elif 'ext4' in legend_tile:
        ax.axvline(x=3.2, linestyle='-', linewidth=2, color='blue')
        ax.annotate("16 GB, physical RAM",
            xy=(3.2, 43), xycoords='data',
            xytext=(5.2, 43), textcoords='data',
            size=10, va="center", ha="left",
            arrowprops=dict(arrowstyle="simple"))
    elif 'Lustre old manager' in legend_tile:
        ax.axvline(x=3.2, linestyle='-', linewidth=2, color='blue')
        ax.annotate("16 GB, physical RAM",
            xy=(3.2, 43), xycoords='data',
            xytext=(5.2, 43), textcoords='data',
            size=10, va="center", ha="left",
            arrowprops=dict(arrowstyle="simple"))
    # elif 'Lustre new ADV Manager IO replay FIXED' in legend_tile:
    #     ax.axvline(x=3.2, linestyle='-', linewidth=2, color='blue')
    #     ax.annotate("16 GB, physical RAM",
    #         xy=(3.2, 43), xycoords='data',
    #         xytext=(5.2, 43), textcoords='data',
    #         size=10, va="center", ha="left",
    #         arrowprops=dict(arrowstyle="simple"))

    plt.gca().xaxis.grid(True)  # enable or disable vertical grid lines
    plt.gca().yaxis.grid(True)  # enable or disable horizontal grid lines
    ax.set_xlim([0, 20])
    #ax.set_ylim([-70, 410])  # same y axis scale for every plot

    #ax.spines["right"].set_visible(False)
    #ax.spines["top"].set_visible(False)
    #ax.tick_params(axis='both', direction='out')
    #ax.get_xaxis().tick_bottom()   # remove unneeded ticks
    #ax.get_yaxis().tick_left()
    ax.yaxis.grid(False) #vertical lines
    ax.xaxis.grid(False) #horizontal lines

    #plt.gca().xaxis.x_lim([0, 20])
    l = ax.legend(loc=(0.4, 0.55), shadow=True, prop={'size': 'x-small'}, fontsize=11, title=legend_tile)
    plt.setp(l.get_title(), fontsize=10)  # trick to set legend title font size
    #plt.subplots_adjust(top=.91)
    #plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
    plt.tight_layout()

    plt.show()


def plot_line_points_percentage_all_metrics2(x, y1, y2, y_throu_true, y_throu_false, y_reads_true, y_reads_false, y1_err, y2_err, y_reads_false_client, y_stdreads_false_client, y_reads_true_client, y_stdreads_true_client, xlabel, ylabel, legend_tile):
    #fig = plt.figure(figsize=(7, 5))
    fig = plt.figure(figsize=(6, 4))
    #fig, ax = plt.subplots(nrows=1, ncols=3, sharex=True, sharey=True)
    ax = fig.add_subplot(111)
    plt.xticks(x, xlabel, fontsize=12)
    plt.yticks(fontsize=14)
    #plt.title('# Operations per month', fontsize=30)
    plt.xlabel('File size [GB]', fontsize=16)
    plt.ylabel(ylabel, fontsize=16)
    #plt.grid(True)
    #ax.spines["right"].set_visible(False)
    #ax.spines["top"].set_visible(False)
    #ax.tick_params(axis='both', direction='out')
    y_runtime = ((y1 - y2)/y2) * 100
    y_reads = ((y_reads_true - y_reads_false)/y_reads_false) * 100
    if 'GPFS' in legend_tile:
        y_reads_client = ((y_reads_true_client - y_reads_false_client)/y_reads_false_client) * 100
    y_thr = ((y_throu_true - y_throu_false)/y_throu_false) * 100

    y_base = []
    for i in range(0, len(y1)):
        y_base.append(0)
    y_baseline = np.array(y_base)

    ax.plot(x, y_runtime, marker='*', linestyle=':', linewidth=1, color='black', label='runtime')
    #ax = fig.add_subplot(111)
    ax.plot(x, y_reads, marker='<', linestyle='-.', linewidth=1, color='black', label='disk server reads')
    ax.plot(x, y_reads_client, marker='x', linestyle='-', linewidth=1, color='black', label='client reads')
    #ax = fig.add_subplot(111)
    ax.plot(x, y_thr, marker='D', linestyle='--', linewidth=1, color='black', label='throughput (server read MB/ runtime)')
    #ax = fig.add_subplot(111)
    ax.plot(x, y_baseline, marker='s', linestyle='-', linewidth=1, color='red', label='baseline NO AM')
    #plt.errorbar(x, y1, y1_err, color='0', label=lab_coord_true, marker='o', linestyle='-', linewidth=2)
    #plt.errorbar(x, y2, y2_err, color='0', label=lab_coord_false, marker='s', linestyle='--', linewidth=2)
    """
    if 'GPFS prefetch enabled' in legend_tile:
        ax.axvline(x=3.2, linestyle='-', linewidth=2, color='blue')
        ax.annotate("16 GB, physical RAM",
            xy=(3.2, 11), xycoords='data',
            xytext=(5.2, 11), textcoords='data',
            size=10, va="center", ha="left",
            arrowprops=dict(arrowstyle="simple"))
    if 'Lustre new ADV Manager' in legend_tile:
        ax.axvline(x=3.2, linestyle='-', linewidth=2, color='blue')
        ax.annotate("16 GB, physical RAM",
            xy=(3.2, 50), xycoords='data',
            xytext=(5.2, 50), textcoords='data',
            size=10, va="center", ha="left",
            arrowprops=dict(arrowstyle="simple"))
    if 'GPFS new ADV Manager WRONG' in legend_tile:
        ax.axvline(x=3.2, linestyle='-', linewidth=2, color='blue')
        ax.annotate("16 GB, physical RAM",
            xy=(3.2, 11), xycoords='data',
            xytext=(5.2, 11), textcoords='data',
            size=10, va="center", ha="left",
            arrowprops=dict(arrowstyle="simple"))
    """
    #if 'GPFS new ADV Manager FIXED' in legend_tile:
    if 'GPFS' in legend_tile:
        ax.axvline(x=3.2, linestyle='-', linewidth=2, color='blue')
        ax.annotate("16 GB, physical RAM",
            xy=(3.2, -70), xycoords='data',
            xytext=(5.2, -70), textcoords='data',
            size=10, va="center", ha="left",
            arrowprops=dict(arrowstyle="simple"))


    plt.gca().xaxis.grid(True)  # enable or disable vertical grid lines
    plt.gca().yaxis.grid(True)  # enable or disable horizontal grid lines
    ax.set_xlim([0, 20])
    ax.set_ylim([-100, 40])  # same y axis scale for every plot

    #ax.spines["right"].set_visible(False)
    #ax.spines["top"].set_visible(False)
    #ax.tick_params(axis='both', direction='out')
    #ax.get_xaxis().tick_bottom()   # remove unneeded ticks
    #ax.get_yaxis().tick_left()
    ax.yaxis.grid(False) #vertical lines
    ax.xaxis.grid(False) #horizontal lines

    #plt.gca().xaxis.x_lim([0, 20])
    l = ax.legend(loc=(0.4, 0.26), shadow=True, prop={'size': 'x-small'}, fontsize=11, title=legend_tile)
    plt.setp(l.get_title(), fontsize=10)  # trick to set legend title font size
    #plt.subplots_adjust(top=.91)
    #plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
    plt.tight_layout()

    plt.show()


# def plotbareverything(x_axis, tags, runtime_false, runtime_false_err, runtime_true, runtime_true_err, ylabel, xticks, legend_title):
#     #N = len(runtime_false)
#
#     #ind = np.arange(N)  # the x locations for the groups
#     width_a = []       # the width of the bars
#     for i in range(0, len(runtime_true)):
#         width_a.append(0.35)
#     width = np.array(width_a)
#     fig, ax = plt.subplots()
#     rects1 = ax.bar(x_axis-width, runtime_false, width, color='0.7', yerr=runtime_false_err, ecolor='0')
#
#
#     rects2 = ax.bar(x_axis, runtime_true, width, color='0.1', yerr=runtime_true_err, ecolor='0')
#
#     # add some text for labels, title and axes ticks
#     ax.set_ylabel(ylabel, fontsize=14)
#     ax.set_xlim([0, 11])
#     plt.xlabel('File size [GB]', fontsize=14)
#     #ax.set_title('Scores by group and gender')
#     #ax.set_xticks(x_axis, tags)
#     #xticks_f = tuple(xticks)
#     #ax.set_xticklabels(tags)
#     plt.xticks(x_axis, tags)
#     if 'throughput' not in ylabel:
#         ax.legend( (rects1[0], rects2[0]), ('w/o AIO', 'w/ AIO'), fancybox=True, loc='upper left', fontsize=13, title=legend_title)
#     plt.tight_layout()
#     plt.show()



def plotbareverything(x_axis, tags, runtime_false, runtime_false_err, runtime_true, runtime_true_err, ylabel, xticks, legend_title):
    #N = len(runtime_false)

    #ind = np.arange(N)  # the x locations for the groups
    width_a = []       # the width of the bars
    for i in range(0, len(runtime_true)):
        width_a.append(0.35)
    width = np.array(width_a)
    fig, ax = plt.subplots()
    #rects1 = ax.bar(x_axis-width, runtime_false, width, color='0.7', yerr=runtime_false_err, ecolor='0')
    plt.errorbar(x_axis, runtime_false, marker='x', markersize=5, yerr=runtime_false_err, ecolor='0', linestyle='-', color='black', label='w/o SAIO')
    plt.errorbar(x_axis, runtime_true, marker='o', markersize=5, yerr=runtime_true_err, ecolor='0', linestyle='--', color='black', label='w/ SAIO')

    #rects2 = ax.bar(x_axis, runtime_true, width, color='0.1', yerr=runtime_true_err, ecolor='0')

    # add some text for labels, title and axes ticks
    ax.set_ylabel(ylabel, fontsize=18)
    ax.set_xlim([0, 11])
    plt.xlabel('File size [GB]', fontsize=18)
    #ax.set_title('Scores by group and gender')
    #ax.set_xticks(x_axis, tags)
    #xticks_f = tuple(xticks)
    #ax.set_xticklabels(tags)
    plt.xticks(x_axis, tags)
    plt.setp(ax.yaxis.get_majorticklabels(), fontsize=13)

    l = plt.legend(loc='upper left', title=legend_title, fancybox=True, fontsize=14)
    plt.setp(l.get_title(), fontsize=15)  # trick to set legend title font size
    #if 'throughput' not in ylabel:
    #    ax.legend( (rects1[0], rects2[0]), ('w/o AIO', 'w/ AIO'), fancybox=True, loc='upper left', fontsize=13, title=legend_title)
    plt.tight_layout()
    plt.show()



if __name__ == '__main__':

    mogon = False
    # I'm being lazy at the moemnt for the list of filenames, next iteration of the program will take this files as input parameters...
    # should take title legend from somewhere....
    list_of_summary_results_to_loop_on = [#'summary_GPFS_test_cluster_CCGRID2015_GPFS_prefetch_enabled.json',
                                         #'summary_GPFS_test_cluster_CCGRID2015_GPFS_prefetch_disabled.json',
                                        #'summary_results_24October2014_ext4_differentfilesizes.json',
                                        #'lustre_results_test_cluster_allfilesizes_8November2014.json',
                                        #'summary_GPFS_replay_Tim_implemenalgo_13November2014.json',
                                        #'summary_GPFSprefetch0_replay_Tim_implemenalgo_19November2014.json',
                                        #'summary_GPFSprefetch1_replay_Tim_implemenalgo_19November2014.json',
                                        #'summary_GPFSprefetch2_replay_Tim_implemenalgo_19November2014.json',
                                        #'summary_GPFSprefetch3_replay_Tim_implemenalgo_19November2014.json',
                                        #'summary_GPFSprefetch4_replay_Tim_implemenalgo_19November2014.json',
                                        #'summary_new_ADVMANAGER_GPFS_onerun_preliminary.json',
                                        #'summary_new_ADVMANAGER_GPFS_onerun_preliminary_FIXED.json'
                                        #'summary_GPFS_prefetchlevel2_IOreplay_NEWADVMANAGER_FIXED.json',
                                        #'summary_3runs_per_file_stats_vs_filesizes_GPFS_SAIO_cachesize_8_readaheadsize_4.json',
                                        #'summary_3runs_per_file_stats_vs_filesizes_GPFS_libSAIO_cachesize_8_readaheadsize_4_reduced_13Feb2015.json']
                                        'summary_3runs_per_file_stats_vs_filesizes_ext4_libSAIO_cachesize_8_readaheadsize_4_reduced_14Feb2015.json']
                                        #'summary_3runs_per_file_stats_vs_filesizes_Lustre_libSAIO_cachesize_8_readaheadsize_4_reduced_2March2015.json']
                                        #'summary_mogon_GPFS_libSAIO_varyingfilesizes_reduced_readahead_4_cachesize_8_13Feb2015.json']
                                        #'summary_mogon_GPFS_libSAIO_varyingfilesizes_reduced_readahead_4_cachesize_8_20Feb2015.json']
                                        #'summary_3runs_per_file_stats_vs_filesizes_GPFS_libAIO_cachesize_8_readaheadsize_4.json']
                                        #'summary_GPFS_final_ROOT_NEWADVMANAGER_FIXED.json',
                                        #'summary_Lustre_final_ROOT_NEWADVMANAGER_FIXED.json']
                                        #'summary_Lustre_IOreplay_NEWADVMANAGER_FIXED.json']  #,
                                        #'summary_new_ADVMANAGER_Lustre_onerun_preliminary.json']
    #list_of_legend_titles = ['GPFS prefetch enabled', 'GPFS prefetch disabled', 'ext4', 'Lustre', 'GPFS replay Tim old', 'GPFS replay prefetch0', 'GPFS replay prefetch1', 'GPFS replay prefetch2', 'GPFS replay prefetch3', 'GPFS replay prefetch4', 'GPFS new ADV Manager WRONG', 'GPFS new ADV Manager FIXED', 'Lustre new ADV Manager']
    #list_of_legend_titles = ['GPFS new ADV Manager IO replay FIXED', 'Lustre new ADV Manager IO replay FIXED']
    for ehy in list_of_summary_results_to_loop_on:
        if 'ext4' in ehy:
            if mogon is True:
                list_of_legend_titles = ['ext4 new ADV Manager FULL Run - Mogon' ]
            else:
                list_of_legend_titles = ['ext4 new ADV Manager FULL Run - Test cluster' ]  #, 'ext4 new ADV Manager FULL Run']
        elif 'GPFS' in ehy:
            if mogon is True:
                list_of_legend_titles = ['GPFS new ADV Manager FULL Run - Mogon' ]
            else:
                list_of_legend_titles = ['GPFS new ADV Manager FULL Run - Test cluster' ]
        elif 'Lustre' in ehy:
            if mogon is True:
                list_of_legend_titles = ['Lustre new ADV Manager FULL Run - Mogon' ]
            else:
                list_of_legend_titles = ['Lustre new ADV Manager FULL Run - Test cluster' ]
        #, 'Lustre new ADV Manager FULL Run']


    #list_of_y_labels = [r"$\frac{Y(with\, AM)-Y(NO\, AM)}{Y(NO\, AM)}\cdot 100\, (\%)$"]  # original
    #list_of_y_labels = [r"$\frac{Y_{AM}-Y_{NO\, AM}}{Y_{NO\, AM}}\cdot 100\, (\%)$"]
    list_of_y_labels = [r"$\frac{Y(AM)-Y(NO\, AM)}{Y(NO\, AM)}\cdot 100\, (\%)$"]
    for k in range(0, len(list_of_summary_results_to_loop_on)):

    #file = 'summary_results_24October2014_ext4_differentfilesizes.json'  # test cluster
    #file = 'summary_GPFS_test_cluster_CCGRID2015_GPFS_prefetch_enabled.json'   # test cluster
    #file = 'summary_GPFS_test_cluster_CCGRID2015_GPFS_prefetch_disabled.json'   # test cluster


        reduced = True
        ### prepare lists for plotting... I can put this list outside the loop so that I don't instatiate for every file I read...
        if reduced is False:
            L2 = ['5GB', '10GB', '15GB', '20GB', '25GB', '30GB', '35GB', '40GB', '45GB', '50GB',
              '55GB', '60GB', '65GB', '70GB', '75GB', '80GB', '85GB', '90GB', '95GB']
        else:
            L2 = ['5GB', '15GB', '25GB', '35GB', '45GB', '55GB', '65GB', '75GB', '85GB', '95GB']


        mean_runtime_AM_true_final = []
        mean_runtime_AM_false_final = []
        if 'GPFS' in list_of_summary_results_to_loop_on[k] or 'ext4' in list_of_summary_results_to_loop_on[k] or 'Lustre' in list_of_summary_results_to_loop_on[k]:
            if mogon is False:
                mean_reads_AM_true_final = []
                mean_reads_AM_false_final = []
        if 'GPFS' in list_of_summary_results_to_loop_on[k]:
            mean_reads_AM_true_final_client = []
            mean_reads_AM_false_final_client = []

        #mean_readbytes_AM_true_final = []
        #mean_readbytes_AM_true_final []
        if 'GPFS' in list_of_summary_results_to_loop_on[k] or 'ext4' in list_of_summary_results_to_loop_on[k] or 'Lustre' in list_of_summary_results_to_loop_on[k]:
            if mogon is False:
                mean_thr_AM_true_final = []
                mean_thr_AM_false_final = []

        std_runtime_AM_true_final = []
        std_runtime_AM_false_final = []
        if 'GPFS' in list_of_summary_results_to_loop_on[k] or 'ext4' in list_of_summary_results_to_loop_on[k] or 'Lustre' in list_of_summary_results_to_loop_on[k]:
            if mogon is False:
                std_reads_AM_true_final = []
                std_reads_AM_false_final = []
        if 'GPFS' in list_of_summary_results_to_loop_on[k]:
            std_reads_AM_true_final_client = []
            std_reads_AM_false_final_client = []

        #mean_readbytes_AM_true_final = []
        #mean_readbytes_AM_true_final []
        if 'GPFS' in list_of_summary_results_to_loop_on[k] or 'ext4' in list_of_summary_results_to_loop_on[k] or 'Lustre' in list_of_summary_results_to_loop_on[k]:
            if mogon is False:
                std_thr_AM_true_final = []
                std_thr_AM_false_final = []

        with open(list_of_summary_results_to_loop_on[k], 'r') as fi:
            dict_with_results = json.load(fi)

        tags = []
        x_axis = []
        g = 1

        for j in L2:
            tags.append(j[:-2])
            x_axis.append(g)
            mean_runtime_AM_true_final.append(dict_with_results["AM_True"]["%s" % j]["runtime"])
            mean_runtime_AM_false_final.append(dict_with_results["AM_False"]["%s" % j]["runtime"])
            #if 'GPFS' in list_of_summary_results_to_loop_on[k] and mogon is False:
            if 'GPFS' in list_of_summary_results_to_loop_on[k] or 'ext4' in list_of_summary_results_to_loop_on[k] or 'Lustre' in list_of_summary_results_to_loop_on[k]:
                if mogon is False:
                    mean_reads_AM_true_final.append(dict_with_results["AM_True"]["%s" % j]["reads_server"])
                    mean_reads_AM_false_final.append(dict_with_results["AM_False"]["%s" % j]["reads_server"])
            if 'GPFS' in list_of_summary_results_to_loop_on[k]:
                mean_reads_AM_true_final_client.append(dict_with_results["AM_True"]["%s" % j]["reads_client"])
                mean_reads_AM_false_final_client.append(dict_with_results["AM_False"]["%s" % j]["reads_client"])
            if 'GPFS' in list_of_summary_results_to_loop_on[k] or 'ext4' in list_of_summary_results_to_loop_on[k] or 'Lustre' in list_of_summary_results_to_loop_on[k]:
                if mogon is False:
                    mean_thr_AM_true_final.append(dict_with_results["AM_True"]["%s" % j]["thr"]/MB)
                    mean_thr_AM_false_final.append(dict_with_results["AM_False"]["%s" % j]["thr"]/MB)

            std_runtime_AM_true_final.append(dict_with_results["AM_True"]["%s" % j]["std_runtime"])
            std_runtime_AM_false_final.append(dict_with_results["AM_False"]["%s" % j]["std_runtime"])
            if 'GPFS' in list_of_summary_results_to_loop_on[k] or 'ext4' in list_of_summary_results_to_loop_on[k] or 'Lustre' in list_of_summary_results_to_loop_on[k]:
                if mogon is False:
                    std_reads_AM_true_final.append(dict_with_results["AM_True"]["%s" % j]["std_reads_server"])
                    std_reads_AM_false_final.append(dict_with_results["AM_False"]["%s" % j]["std_reads_server"])
            if 'GPFS' in list_of_summary_results_to_loop_on[k]:
                std_reads_AM_true_final_client.append(dict_with_results["AM_True"]["%s" % j]["std_reads_client"])
                std_reads_AM_false_final_client.append(dict_with_results["AM_False"]["%s" % j]["std_reads_client"])
            if 'GPFS' in list_of_summary_results_to_loop_on[k] or 'ext4' in list_of_summary_results_to_loop_on[k] or 'Lustre' in list_of_summary_results_to_loop_on[k]:
                if mogon is False:
                    std_thr_AM_true_final.append(dict_with_results["AM_True"]["%s" % j]["std_thr"]/MB)
                    std_thr_AM_false_final.append(dict_with_results["AM_False"]["%s" % j]["std_thr"]/MB)

            g += 1


        #print x_axis




        #### prepare numpy arrays (y) to plot
        y_runtime_false = np.array(mean_runtime_AM_false_final)
        y_stdruntime_false = np.array(std_runtime_AM_false_final)
        y_runtime_true = np.array(mean_runtime_AM_true_final)
        y_stdruntime_true = np.array(std_runtime_AM_true_final)
        if 'GPFS' in list_of_summary_results_to_loop_on[k] or 'ext4' in list_of_summary_results_to_loop_on[k] or 'Lustre' in list_of_summary_results_to_loop_on[k]:
            if mogon is False:
                y_reads_false = np.array(mean_reads_AM_false_final)
                y_stdreads_false = np.array(std_reads_AM_false_final)
                y_reads_true = np.array(mean_reads_AM_true_final)
                y_stdreads_true = np.array(std_reads_AM_true_final)
        if 'GPFS' in list_of_summary_results_to_loop_on[k]:
            y_reads_false_client = np.array(mean_reads_AM_false_final_client)
            y_stdreads_false_client = np.array(std_reads_AM_false_final_client)
            y_reads_true_client = np.array(mean_reads_AM_true_final_client)
            y_stdreads_true_client = np.array(std_reads_AM_true_final_client)

        #print y_runtime_true
        if 'GPFS' in list_of_summary_results_to_loop_on[k] or 'ext4' in list_of_summary_results_to_loop_on[k] or 'Lustre' in list_of_summary_results_to_loop_on[k]:
            if mogon is False:
                y_thr_false = np.array(mean_thr_AM_false_final)
                y_std_thr_false = np.array(std_thr_AM_false_final)
                y_thr_true = np.array(mean_thr_AM_true_final)
                y_std_thr_true = np.array(std_thr_AM_true_final)

        if 'GPFS' in list_of_summary_results_to_loop_on[k]:
            plotbareverything(x_axis, tags, y_runtime_false, y_stdruntime_false, y_runtime_true, y_stdruntime_true, 'runtime [sec]', L2, 'GPFS')
            if 'GPFS' in list_of_summary_results_to_loop_on[k] and mogon is False:
                plotbareverything(x_axis, tags, y_reads_false, y_stdreads_false, y_reads_true, y_stdreads_true, 'server reads', L2, 'GPFS')
                plotbareverything(x_axis, tags, y_thr_false, y_std_thr_false, y_thr_true, y_std_thr_true, 'server throughput', L2, 'GPFS')
            plotbareverything(x_axis, tags, y_reads_false_client, y_stdreads_false_client, y_reads_true_client, y_stdreads_true_client, 'client reads', L2, 'GPFS')
        elif 'Lustre' in list_of_summary_results_to_loop_on[k]:
            plotbareverything(x_axis, tags, y_runtime_false, y_stdruntime_false, y_runtime_true, y_stdruntime_true, 'runtime [sec]', L2, 'Lustre')
            plotbareverything(x_axis, tags, y_reads_false, y_stdreads_false, y_reads_true, y_stdreads_true, 'server reads', L2, 'Lustre')
            plotbareverything(x_axis, tags, y_thr_false, y_std_thr_false, y_thr_true, y_std_thr_true, 'server throughput', L2, 'Lustre')
        elif 'ext' in list_of_summary_results_to_loop_on[k]:
            plotbareverything(x_axis, tags, y_runtime_false, y_stdruntime_false, y_runtime_true, y_stdruntime_true, 'runtime [sec]', L2, 'ext4')
            plotbareverything(x_axis, tags, y_reads_false, y_stdreads_false, y_reads_true, y_stdreads_true, 'server reads', L2, 'ext4')
            plotbareverything(x_axis, tags, y_thr_false, y_std_thr_false, y_thr_true, y_std_thr_true, 'server throughput', L2, 'ext4')
        #plot_line_points(x_axis, y_runtime_true, y_runtime_false, y_stdruntime_true, y_stdruntime_false, tags, 'AM true', 'AM false', 'Execution time [s]')
        #plot_line_points(x_axis, y_reads_true, y_reads_false, y_stdreads_true, y_stdreads_false, tags, 'AM true', 'AM false', 'reads/s')
        #plot_line_points(x_axis, y_thr_true, y_thr_false, y_std_thr_true, y_std_thr_false, tags, 'AM true', 'AM false', 'Throughput [MB/s]')

        #barplot_seaborn_difference(x_axis, y_runtime_true, y_runtime_false, y_stdruntime_true, y_stdruntime_false, tags, 'AM true', 'AM false', ' % Execution time [s]')
        #barplot_seaborn_difference(x_axis, y_reads_true, y_reads_false, y_stdreads_true, y_stdreads_false, tags, 'AM true', 'AM false', ' % reads/s')
        #barplot_seaborn_difference(x_axis, y_thr_true, y_thr_false, y_std_thr_true, y_std_thr_false, tags, 'AM true', 'AM false', ' % Throughput [MB/s]')

        #plot_line_points_percentage(x_axis, y_runtime_true, y_runtime_false, y_stdruntime_true, y_stdruntime_false, tags, 'AM true', 'AM false', ' % Execution time [s]')
        #plot_line_points_percentage(x_axis, y_reads_true, y_reads_false, y_stdreads_true, y_stdreads_false, tags, 'AM true', 'AM false', ' % reads/s')
        #plot_line_points_percentage(x_axis, y_thr_true, y_thr_false, y_std_thr_true, y_std_thr_false, tags, 'AM true', 'AM false', ' % Throughput [MB/s]')
        if 'GPFS' in list_of_summary_results_to_loop_on[k]:
            plot_line_points_percentage_all_metrics2(x_axis, y_runtime_true, y_runtime_false, y_thr_true, y_thr_false, y_reads_true, y_reads_false, y_stdruntime_true, y_stdruntime_true, y_reads_false_client, y_stdreads_false_client, y_reads_true_client, y_stdreads_true_client, tags, list_of_y_labels[0], list_of_legend_titles[k])
        else:
        ####### here plot everything: every results summary you got!
            plot_line_points_percentage_all_metrics(x_axis, y_runtime_true, y_runtime_false, y_thr_true, y_thr_false, y_reads_true, y_reads_false, y_stdruntime_true, y_stdruntime_true, tags, list_of_y_labels[0], list_of_legend_titles[k])

        #plot_line_points_percentage_all_metrics(x_axis, y_runtime_true, y_runtime_false, y_thr_true, y_thr_false, y_reads_true, y_reads_false, y_stdruntime_true, y_stdruntime_true, tags, r"$\frac{metric(with\, AM)-metric(NO\, AM)}{metric(NO\, AM)}\cdot 100\, (\%)$", 'GPFS prefetch enabled')
        #plot_line_points_percentage_all_metrics(x_axis, y_runtime_true, y_runtime_false, y_thr_true, y_thr_false, y_reads_true, y_reads_false, y_stdruntime_true, y_stdruntime_true, tags, r"$\frac{metric(with\, AM)-metric(NO\, AM)}{metric(NO\, AM)}\cdot 100\, (\%)$", 'GPFS prefetch disabled')
        #plot_line_points_percentage_all_metrics(x_axis, y_runtime_true, y_runtime_false, y_thr_true, y_thr_false, y_reads_true, y_reads_false, y_stdruntime_true, y_stdruntime_true, tags, r"$\frac{metric(with\, AM)-metric(NO\, AM)}{metric(NO\, AM)}\cdot 100\, (\%)$", 'ext4')

        #plot_line_points_percentage_all_metrics(x, y1, y2, y_throu_true, y_throu_false, y_reads_true, y_reads_false, y1_err, y2_err, xlabel, ylabel)
        # $dfrac{metric(AM)-metric(normal run)}{metric(normal run)}*100$ (%)
        #r"$\displaystyle\sum_{n=1}^\infty\frac{-e^{i\pi}}{2^n}$!"