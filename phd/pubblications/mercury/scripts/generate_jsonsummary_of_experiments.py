#!/usr/bin/env python

__author__ = 'padua'


import os
import argparse
import json
import numpy as np

ext4 = True   # it holds for GPFS too

KB = 1024
MB = KB * 1024
GB = MB * 1024
TB = GB * 1024


def argparse_of_program():
    parser = argparse.ArgumentParser(description='This script generates json summaries for all tests, ready to be plotted')

    parser.add_argument('-d', '--dir', help='Input directory where all results are', required=True)
    parser.add_argument('-o', '--outputjson', help='Output json file name with summary of results', required=True)
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
        if ext4 is True:
            server_reads = findings["reads"]
        else:
            server_reads = findings["reads_server"]
        return server_reads


def read_read_bytes(path_file):
    with open(path_file, 'r') as f:
        findings = json.load(f)
        if ext4 is True:
            server_reads = findings["read bytes"]
        else:
            server_reads = findings["read_bytes_server"]
        return server_reads


if __name__ == '__main__':

    arg_of_program = argparse_of_program()   #get the parameters (dir with results)

    L1 = ['AM_True', 'AM_False']
    L2 = ['5GB', '10GB', '15GB', '20GB', '25GB', '30GB', '35GB', '40GB', '45GB', '50GB',
          '55GB', '60GB', '65GB', '70GB', '75GB', '80GB', '85GB', '90GB', '95GB']
    list_of_input_filenames = [
        '00050', 'huge_new_file_2sources', 'huge_new_file_3sources',
        'huge_new_file_4sources', 'huge_new_file_5sources', 'huge_new_file_6sources',
        'huge_new_file_7sources', 'huge_new_file_8sources', 'huge_new_file_9sources',
        'huge_new_file_10sources', 'huge_new_file_11sources', 'huge_new_file_12sources',
        'huge_new_file_13sources', 'huge_new_file_14sources', 'huge_new_file_15sources',
        'huge_new_file_16sources', 'huge_new_file_17sources', 'huge_new_file_18sources',
        'huge_new_file_19sources']


    ###### create dict to hold the values ######
    ### dictionary to hold the final data to plot!
    dict_with_results = {}
    for l1 in L1:
        dict_with_results[l1] = {}

    for l1 in L1:
        for l2 in L2:
            #my_dict[l1][l2] = res_list
            dict_with_results[l1][l2] = {}


    list_of_list_AM_false_runtime = [[] for i in range(0, len(list_of_input_filenames))]
    list_of_list_AM_true_runtime = [[] for i in range(0, len(list_of_input_filenames))]

    list_of_list_AM_false_reads = [[] for i in range(0, len(list_of_input_filenames))]
    list_of_list_AM_false_readbytes = [[] for i in range(0, len(list_of_input_filenames))]

    list_of_list_AM_true_reads = [[] for i in range(0, len(list_of_input_filenames))]
    list_of_list_AM_true_readbytes = [[] for i in range(0, len(list_of_input_filenames))]

    ##### lists with throughput info

    list_of_list_AM_false_throughput = [[] for i in range(0, len(list_of_input_filenames))]
    list_of_list_AM_true_throughput = [[] for i in range(0, len(list_of_input_filenames))]


    cwd = get_cwd()
    abs_path_dir = os.path.join(cwd, arg_of_program.dir)
    subdirs = get_list_of_filesdirindir(abs_path_dir)  # is not absolute path
    for directory in subdirs:
        if 'False' in directory.split("-")[1].split("_"):
            #print("NO AM results")
            for inputfile in list_of_input_filenames:
                if inputfile in directory.split("-")[3].split("."):
                    index_in_list = list_of_input_filenames.index(inputfile)
                    #print(inputfile)
                    result_file = os.path.join((os.path.join(abs_path_dir, directory)), 'results.json')
                    disk_stat_file = os.path.join((os.path.join(abs_path_dir, directory)), 'disk_stats.json')
                    list_of_list_AM_false_runtime[index_in_list].append(read_runtime(result_file))
                    list_of_list_AM_false_reads[index_in_list].append(read_reads_info(disk_stat_file))
                    list_of_list_AM_false_readbytes[index_in_list].append(read_read_bytes(disk_stat_file))
                    list_of_list_AM_false_throughput[index_in_list].append(read_read_bytes(disk_stat_file) / read_runtime(result_file))


        if 'True' in directory.split("-")[1].split("_"):
            #print("AM true")
            for inputfile in list_of_input_filenames:
                if inputfile in directory.split("-")[5].split("."):
                    index_in_list = list_of_input_filenames.index(inputfile)
                    #print("5GB file")
                    result_file = os.path.join((os.path.join(abs_path_dir, directory)), 'results.json')
                    disk_stat_file = os.path.join((os.path.join(abs_path_dir, directory)), 'disk_stats.json')
                    list_of_list_AM_true_runtime[index_in_list].append(read_runtime(result_file))
                    list_of_list_AM_true_reads[index_in_list].append(read_reads_info(disk_stat_file))
                    list_of_list_AM_true_readbytes[index_in_list].append(read_read_bytes(disk_stat_file))
                    list_of_list_AM_true_throughput[index_in_list].append(read_read_bytes(disk_stat_file) / read_runtime(result_file))



    ##### NOW evaluate means and stds for runtime, number of reads and read bytes and evaluate throughput

    filesizes_filenames = zip(L2, list_of_input_filenames)
    index = 0
    for j in L2:
        mean_runtimes_AMfalse = evaluate_mean(list_of_list_AM_false_runtime[index])
        std_runtimes_AMfalse = evaluate_std(list_of_list_AM_false_runtime[index])

        mean_reads_AMfalse = evaluate_mean(list_of_list_AM_false_reads[index])
        std_reads_AMfalse = evaluate_std(list_of_list_AM_false_reads[index])

        mean_readbytes_AMfalse = evaluate_mean(list_of_list_AM_false_readbytes[index])
        std_readbytes_AMfalse = evaluate_std(list_of_list_AM_false_readbytes[index])

        mean_thr_AMfalse = evaluate_mean(list_of_list_AM_false_throughput[index])
        std_thr_AMfalse = evaluate_std(list_of_list_AM_false_throughput[index])

        dict_with_results["AM_False"]["%s" % j]["runtime"] = mean_runtimes_AMfalse    ## get's runtime
        dict_with_results["AM_False"]["%s" % j]["std_runtime"] = std_runtimes_AMfalse
        dict_with_results["AM_False"]["%s" % j]["reads_server"] = mean_reads_AMfalse    ## get's runtime
        dict_with_results["AM_False"]["%s" % j]["std_reads_server"] = std_reads_AMfalse
        dict_with_results["AM_False"]["%s" % j]["readbytes"] = mean_readbytes_AMfalse    ## get's runtime
        dict_with_results["AM_False"]["%s" % j]["std_readbytes"] = std_readbytes_AMfalse
        dict_with_results["AM_False"]["%s" % j]["thr"] = mean_thr_AMfalse    ## get's runtime
        dict_with_results["AM_False"]["%s" % j]["std_thr"] = std_thr_AMfalse


        ### NOW AM True

        mean_runtimes_AMtrue = evaluate_mean(list_of_list_AM_true_runtime[index])
        std_runtimes_AMtrue = evaluate_std(list_of_list_AM_true_runtime[index])

        mean_reads_AMtrue = evaluate_mean(list_of_list_AM_true_reads[index])
        std_reads_AMtrue = evaluate_std(list_of_list_AM_true_reads[index])

        mean_readbytes_AMtrue = evaluate_mean(list_of_list_AM_true_readbytes[index])
        std_readbytes_AMtrue = evaluate_std(list_of_list_AM_true_readbytes[index])

        mean_thr_AMtrue = evaluate_mean(list_of_list_AM_true_throughput[index])
        std_thr_AMtrue = evaluate_std(list_of_list_AM_true_throughput[index])

        dict_with_results["AM_True"]["%s" % j]["runtime"] = mean_runtimes_AMtrue    ## get's runtime
        dict_with_results["AM_True"]["%s" % j]["std_runtime"] = std_runtimes_AMtrue
        dict_with_results["AM_True"]["%s" % j]["reads_server"] = mean_reads_AMtrue    ## get's runtime
        dict_with_results["AM_True"]["%s" % j]["std_reads_server"] = std_reads_AMtrue
        dict_with_results["AM_True"]["%s" % j]["readbytes"] = mean_readbytes_AMtrue    ## get's runtime
        dict_with_results["AM_True"]["%s" % j]["std_readbytes"] = std_readbytes_AMtrue
        dict_with_results["AM_True"]["%s" % j]["thr"] = mean_thr_AMtrue    ## get's runtime
        dict_with_results["AM_True"]["%s" % j]["std_thr"] = std_thr_AMtrue

        index += 1

    with open(arg_of_program.outputjson, 'w') as fp:
        json.dump(dict_with_results, fp)
