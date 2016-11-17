#/usr/bin/env python

import json
import numpy as np
import argparse

### prettify borrowed from Matthias

__author__ = 'padua'


KB = 1024
MB = KB * 1024
GB = MB * 1024
TB = GB * 1024


def argparse_of_program():
    parser = argparse.ArgumentParser(description='This script generates the latex table with all the results')
    parser.add_argument('-o', '--outputtex', help='Absolute path of output tex file with table; e.g. /home/foo/foo/foo.tex', required=True)
    args = parser.parse_args()
    return args


def prettyfy(number):
    d = float(number)
    if d - int(d) > 0:
        return '{:,.2f}'.format(d)
    return '{:,d}'.format(int(d))


if __name__ == '__main__':
    arg_of_program = argparse_of_program()
    filename = arg_of_program.outputtex
    with open(filename, 'w') as f:
        f.write("\\begin{table*}[!h]")
        f.write("\n")
        f.write("\\centering")
        f.write("\n")
        f.write("\\resizebox{\columnwidth}{!}{%")
        f.write("\n")
        #f.write("\\begin{tabular}{@{}rrrrcrrrcrrr@{}}")   # right aligned...choose one
        f.write("\\begin{tabular}{@{}rccccccccccc@{}}")
        f.write("\n")
        f.write("\\toprule")
        f.write("\n")
        f.write("&")
        f.write("\n")
        f.write("\\multicolumn{3}{c}{runtime (sec)} &")
        f.write("\n")
        f.write("\\phantom{abc}&")
        f.write("\n")
        f.write("\\multicolumn{3}{c}{reads} &")
        f.write("\n")
        f.write("\\phantom{abc} &")
        f.write("\n")
        f.write("\\multicolumn{3}{c}{throughput (MB/s)}\n")
        f.write("\\\\")
        f.write("\n")
        f.write("\\cmidrule{2-4}\cmidrule{6-8}\cmidrule{10-12}\n")
        f.write("& ext4 & Lustre & GPFS && ext4 & Lustre & GPFS && ext4 & Lustre & GPFS\\\\")
        f.write("\n")
        f.write("\\midrule\n")
        f.write("\\textbf{No AM}\\\\")
        f.write("\n")
        #f.write("\\\\")


        list_of_summary_results_to_loop_on = ['summary_results_24October2014_ext4_differentfilesizes.json',
                                               'lustre_results_test_cluster_allfilesizes_8November2014.json',
                                                'summary_GPFS_test_cluster_CCGRID2015_GPFS_prefetch_enabled.json']


        for k in range(0, len(list_of_summary_results_to_loop_on)):

            L2 = ['5GB', '10GB', '15GB', '20GB', '25GB', '30GB', '35GB', '40GB', '45GB', '50GB',
                  '55GB', '60GB', '65GB', '70GB', '75GB', '80GB', '85GB', '90GB', '95GB']

            mean_runtime_AM_true_final = []
            mean_runtime_AM_false_final = []

            mean_reads_AM_true_final = []
            mean_reads_AM_false_final = []

            #mean_readbytes_AM_true_final = []
            #mean_readbytes_AM_true_final []

            mean_thr_AM_true_final = []
            mean_thr_AM_false_final = []

            std_runtime_AM_true_final = []
            std_runtime_AM_false_final = []

            std_reads_AM_true_final = []
            std_reads_AM_false_final = []

            #mean_readbytes_AM_true_final = []
            #mean_readbytes_AM_true_final []

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
                mean_reads_AM_true_final.append(dict_with_results["AM_True"]["%s" % j]["reads_server"])
                mean_reads_AM_false_final.append(dict_with_results["AM_False"]["%s" % j]["reads_server"])
                mean_thr_AM_true_final.append(dict_with_results["AM_True"]["%s" % j]["thr"]/MB)
                mean_thr_AM_false_final.append(dict_with_results["AM_False"]["%s" % j]["thr"]/MB)

                std_runtime_AM_true_final.append(dict_with_results["AM_True"]["%s" % j]["std_runtime"])
                std_runtime_AM_false_final.append(dict_with_results["AM_False"]["%s" % j]["std_runtime"])
                std_reads_AM_true_final.append(dict_with_results["AM_True"]["%s" % j]["std_reads_server"])
                std_reads_AM_false_final.append(dict_with_results["AM_False"]["%s" % j]["std_reads_server"])
                std_thr_AM_true_final.append(dict_with_results["AM_True"]["%s" % j]["std_thr"]/MB)
                std_thr_AM_false_final.append(dict_with_results["AM_False"]["%s" % j]["std_thr"]/MB)

                g += 1

            #### prepare numpy arrays (y) to plot
            if k == 0:
                # ext4
                y_runtime_false_ext4 = np.array(mean_runtime_AM_false_final)
                y_stdruntime_false_ext4 = np.array(std_runtime_AM_false_final)
                y_runtime_true_ext4 = np.array(mean_runtime_AM_true_final)
                y_stdruntime_true_ext4 = np.array(std_runtime_AM_true_final)

                y_reads_false_ext4 = np.array(mean_reads_AM_false_final)
                y_stdreads_false_ext4 = np.array(std_reads_AM_false_final)
                y_reads_true_ext4 = np.array(mean_reads_AM_true_final)
                y_stdreads_true_ext4 = np.array(std_reads_AM_true_final)


                y_thr_false_ext4 = np.array(mean_thr_AM_false_final)
                y_std_thr_false_ext4 = np.array(std_thr_AM_false_final)
                y_thr_true_ext4 = np.array(mean_thr_AM_true_final)
                y_std_thr_true_ext4 = np.array(std_thr_AM_true_final)
            elif k == 1:
                # Lustre
                y_runtime_false_Lustre = np.array(mean_runtime_AM_false_final)
                y_stdruntime_false_Lustre = np.array(std_runtime_AM_false_final)
                y_runtime_true_Lustre = np.array(mean_runtime_AM_true_final)
                y_stdruntime_true_Lustre = np.array(std_runtime_AM_true_final)

                y_reads_false_Lustre = np.array(mean_reads_AM_false_final)
                y_stdreads_false_Lustre = np.array(std_reads_AM_false_final)
                y_reads_true_Lustre = np.array(mean_reads_AM_true_final)
                y_stdreads_true_Lustre = np.array(std_reads_AM_true_final)


                y_thr_false_Lustre = np.array(mean_thr_AM_false_final)
                y_std_thr_false_Lustre = np.array(std_thr_AM_false_final)
                y_thr_true_Lustre = np.array(mean_thr_AM_true_final)
                y_std_thr_true_Lustre = np.array(std_thr_AM_true_final)
            elif k == 2:
                #GPFS
                y_runtime_false_gpfs = np.array(mean_runtime_AM_false_final)
                y_stdruntime_false_gpfs = np.array(std_runtime_AM_false_final)
                y_runtime_true_gpfs = np.array(mean_runtime_AM_true_final)
                y_stdruntime_true_gpfs = np.array(std_runtime_AM_true_final)

                y_reads_false_gpfs = np.array(mean_reads_AM_false_final)
                y_stdreads_false_gpfs = np.array(std_reads_AM_false_final)
                y_reads_true_gpfs = np.array(mean_reads_AM_true_final)
                y_stdreads_true_gpfs = np.array(std_reads_AM_true_final)


                y_thr_false_gpfs = np.array(mean_thr_AM_false_final)
                y_std_thr_false_gpfs = np.array(std_thr_AM_false_final)
                y_thr_true_gpfs = np.array(mean_thr_AM_true_final)
                y_std_thr_true_gpfs = np.array(std_thr_AM_true_final)

        h = 0
        for y in L2:

            f.write("$%s$ GB & $%s\pm %s$ & $%s\pm %s$ & $%s\pm %s$ && $%s\pm %s$ & $%s\pm %s$ & $%s\pm %s$ && $%s\pm %s$ & $%s\pm %s$ & $%s\pm %s$\\\\" % (y[:-2], prettyfy(y_runtime_false_ext4[h]), prettyfy(y_stdruntime_false_ext4[h]), prettyfy(y_runtime_false_Lustre[h]),
            prettyfy(y_stdruntime_false_Lustre[h]), prettyfy(y_runtime_false_gpfs[h]), prettyfy(y_stdruntime_false_gpfs[h]), int(y_reads_false_ext4[h]), int(y_stdreads_false_ext4[h]), int(y_reads_false_Lustre[h]), int(y_stdreads_false_Lustre[h]), int(y_reads_false_gpfs[h]), int(y_stdreads_false_gpfs[h]), prettyfy(y_thr_false_ext4[h]),
            prettyfy(y_std_thr_false_ext4[h]), prettyfy(y_thr_false_Lustre[h]), prettyfy(y_std_thr_false_Lustre[h]), prettyfy(y_thr_false_gpfs[h]), prettyfy(y_std_thr_false_gpfs[h])))
            f.write("\n")
            h += 1
        f.write("\\textbf{with AM}")
        f.write("\n")
        f.write("\\\\")
        f.write("\n")
        h = 0
        for y in L2:

            f.write("$%s$ GB & $%s\pm %s$ & $%s\pm %s$ & $%s\pm %s$ && $%s\pm %s$ & $%s\pm %s$ & $%s\pm %s$ && $%s\pm %s$ & $%s\pm %s$ & $%s\pm %s$\\\\" % (y[:-2], prettyfy(y_runtime_true_ext4[h]), prettyfy(y_stdruntime_true_ext4[h]), prettyfy(y_runtime_true_Lustre[h]),
            prettyfy(y_stdruntime_true_Lustre[h]), prettyfy(y_runtime_true_gpfs[h]), prettyfy(y_stdruntime_true_gpfs[h]), int(y_reads_true_ext4[h]), int(y_stdreads_true_ext4[h]), int(y_reads_true_Lustre[h]), int(y_stdreads_true_Lustre[h]), int(y_reads_true_gpfs[h]), int(y_stdreads_true_gpfs[h]), prettyfy(y_thr_true_ext4[h]),
            prettyfy(y_std_thr_true_ext4[h]), prettyfy(y_thr_true_Lustre[h]), prettyfy(y_std_thr_true_Lustre[h]), prettyfy(y_thr_true_gpfs[h]), prettyfy(y_std_thr_false_gpfs[h])))
            f.write("\n")
            h += 1

        f.write("\\bottomrule")
        f.write("\n")
        f.write("\\end{tabular}%")
        f.write("\n")
        f.write("}")
        f.write("\n")
        f.write("\\caption{Test cluster results}")
        f.write("\n")
        f.write("\\end{table*}")
