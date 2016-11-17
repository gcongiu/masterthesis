__author__ = 'Federico G. Padua'


import os
import argparse
import csv
#import sys
import numpy

# "fancy" stuff
pm = u"\u00B1"
ch = pm.encode('utf-8')

# helper for evaluating mean and std of a list of values
def calculate_avg_std_given_a_list(list_toevaluate_avgstd_from):
    temp_array = numpy.array(list_toevaluate_avgstd_from)
    temp_avg = numpy.mean(temp_array)
    temp_std = numpy.std(temp_array)
    return temp_avg, temp_std

# helper for printing mean \pm std in the usual scientific/paper way with Latex
# symbol
def print_mean_and_std(mean_s, std_s):
    print("%s %s %s" % (mean_s, ch, std_s))

# helper for reading columns of csv files
def csv_dict_reader(file_obj, list_reads): #, list_kBread):

    reader = csv.DictReader(file_obj, delimiter=' ')

    for line in reader:

        list_reads.append(line["[OST]Read"])
        #list_kBread.append(line["[OST]ReadKB"])
        #print(line["[CLT]ReadKB"])
    return list_reads #, list_kBread

#lustre_dir_reads_server = 'lustre_reads_dir'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='This script generates preprocess LUSTRE reads traces, ready for averages and stds', version='0.0')
    parser.add_argument('-d', '--dir', help='Directory where LUSTRE read() OST or client traces are.', required=True)
    args = parser.parse_args()
    dir_LUSTRE_read_traces = args.dir
    lustre_dir_full_path = os.path.join(os.getcwd(), dir_LUSTRE_read_traces)
    list_of_trace_files = os.listdir(lustre_dir_full_path)
    # lists for different files and configs
    list_reads_lustre_file00050_NOAM = []
    list_reads_lustre_file00050_tailored = []
    list_reads_lustre_file00050_sliding_wind = []

    list_reads_lustre_file00035_NOAM = []
    list_reads_lustre_file00035_tailored = []
    list_reads_lustre_file00035_sliding_wind = []

    list_reads_lustre_file00186_NOAM = []
    list_reads_lustre_file00186_tailored = []
    list_reads_lustre_file00186_sliding_wind = []

    list_filenames_match = ['00050.root_NOCONF', '00035.root_NOCONF', '00186.root_NOCONF',
                            '00050.root_config_00050_tailored', '00035.root_config_00035_tailored',
                            '00186.root_config_00186_tailored',
                            '00050.root_config_00050.json', '00035.root_config_00035.json', '00186.root_config_00186.json']

    list_sums_00050_NOAM = []
    list_sums_00035_NOAM = []
    list_sums_00186_NOAM = []

    list_sums_00050_tailored = []
    list_sums_00035_tailored = []
    list_sums_00186_tailored = []

    list_sums_00050_sld = []
    list_sums_00035_sld = []
    list_sums_00186_sld = []

    total_reads_00050_NOAM = []
    res_00050_NOAM = []
    total_reads_00035_NOAM = []
    res_00035_NOAM = []
    total_reads_00186_NOAM = []
    res_00186_NOAM = []

    total_reads_00050_tailored = []
    res_00050_tailored = []
    total_reads_00035_tailored = []
    res_00035_tailored = []
    total_reads_00186_tailored = []
    res_00186_tailored = []

    total_reads_00050_sld = []
    res_00050_sld = []
    total_reads_00035_sld = []
    res_00035_sld = []
    total_reads_00186_sld = []
    res_00186_sld = []



    for filename in list_of_trace_files:
        with open(os.path.join(lustre_dir_full_path, filename)) as f_obj:
            if filename[0:17] == list_filenames_match[0]:
                csv_dict_reader(f_obj, list_reads_lustre_file00050_NOAM)
                total_reads_00050_NOAM = list(map(int, list_reads_lustre_file00050_NOAM))
                #print total_reads_00050
                res_00050_NOAM = sum(total_reads_00050_NOAM)
                #print res_00050
                list_sums_00050_NOAM.append(res_00050_NOAM)
                #print list_sums_00050_NOAM
                #print list_reads_lustre_file00050_NOAM
                del list_reads_lustre_file00050_NOAM[:]
                del total_reads_00050_NOAM
                del res_00050_NOAM
            elif filename[0:17] == list_filenames_match[1]:
                csv_dict_reader(f_obj, list_reads_lustre_file00035_NOAM)
                total_reads_00035_NOAM = list(map(int, list_reads_lustre_file00035_NOAM))
                res_00035_NOAM = sum(total_reads_00035_NOAM)
                list_sums_00035_NOAM.append(res_00035_NOAM)
                del list_reads_lustre_file00035_NOAM[:]
                del total_reads_00035_NOAM
                del res_00035_NOAM
            elif filename[0:17] == list_filenames_match[2]:
                csv_dict_reader(f_obj, list_reads_lustre_file00186_NOAM)
                total_reads_00186_NOAM = list(map(int, list_reads_lustre_file00186_NOAM))
                res_00186_NOAM = sum(total_reads_00186_NOAM)
                list_sums_00186_NOAM.append(res_00186_NOAM)
                del list_reads_lustre_file00186_NOAM[:]
                del total_reads_00186_NOAM
                del res_00186_NOAM

                # now tailored
            elif filename[0:32] == list_filenames_match[3]:
                csv_dict_reader(f_obj, list_reads_lustre_file00050_tailored)
                total_reads_00050_tailored = list(map(int, list_reads_lustre_file00050_tailored))
                #print total_reads_00050
                res_00050_tailored = sum(total_reads_00050_tailored)
                #print res_00050
                list_sums_00050_tailored.append(res_00050_tailored)
                #print list_sums_00050_NOAM
                #print list_reads_lustre_file00050_NOAM
                del list_reads_lustre_file00050_tailored[:]
                del total_reads_00050_tailored
                del res_00050_tailored
            elif filename[0:32] == list_filenames_match[4]:
                csv_dict_reader(f_obj, list_reads_lustre_file00035_tailored)
                total_reads_00035_tailored = list(map(int, list_reads_lustre_file00035_tailored))
                res_00035_tailored = sum(total_reads_00035_tailored)
                list_sums_00035_tailored.append(res_00035_tailored)
                del list_reads_lustre_file00035_tailored[:]
                del total_reads_00035_tailored
                del res_00035_tailored
            elif filename[0:32] == list_filenames_match[5]:
                csv_dict_reader(f_obj, list_reads_lustre_file00186_tailored)
                total_reads_00186_tailored = list(map(int, list_reads_lustre_file00186_tailored))
                res_00186_tailored = sum(total_reads_00186_tailored)
                list_sums_00186_tailored.append(res_00186_tailored)
                del list_reads_lustre_file00186_tailored[:]
                del total_reads_00186_tailored
                del res_00186_tailored

                #now slid wind

            if filename[0:28] == list_filenames_match[6]:
                csv_dict_reader(f_obj, list_reads_lustre_file00050_sliding_wind)
                total_reads_00050_sld = list(map(int, list_reads_lustre_file00050_sliding_wind))
                #print total_reads_00050
                res_00050_sld = sum(total_reads_00050_sld)
                #print res_00050
                list_sums_00050_sld.append(res_00050_sld)
                print list_sums_00050_sld
                #print list_reads_lustre_file00050_NOAM
                del list_reads_lustre_file00050_sliding_wind[:]
                del total_reads_00050_sld
                del res_00050_sld
            elif filename[0:28] == list_filenames_match[7]:
                csv_dict_reader(f_obj, list_reads_lustre_file00035_sliding_wind)
                total_reads_00035_sld = list(map(int, list_reads_lustre_file00035_sliding_wind))
                res_00035_sld = sum(total_reads_00035_sld)
                list_sums_00035_sld.append(res_00035_sld)
                del list_reads_lustre_file00035_sliding_wind[:]
                del total_reads_00035_sld
                del res_00035_sld
            elif filename[0:28] == list_filenames_match[8]:
                csv_dict_reader(f_obj, list_reads_lustre_file00186_sliding_wind)
                total_reads_00186_sld = list(map(int, list_reads_lustre_file00186_sliding_wind))
                res_00186_sld = sum(total_reads_00186_sld)
                list_sums_00186_sld.append(res_00186_sld)
                del list_reads_lustre_file00186_sliding_wind[:]
                del total_reads_00186_sld
                del res_00186_sld

    # evaluate averages and stds now

    avg_reads_00050_NOAM, std_reads_00050_NOAM = calculate_avg_std_given_a_list(list_sums_00050_NOAM)
    avg_reads_00035_NOAM, std_reads_00035_NOAM = calculate_avg_std_given_a_list(list_sums_00035_NOAM)
    avg_reads_00186_NOAM, std_reads_00186_NOAM = calculate_avg_std_given_a_list(list_sums_00186_NOAM)

    avg_reads_00050_tailored, std_reads_00050_tailored = calculate_avg_std_given_a_list(list_sums_00050_tailored)
    avg_reads_00035_tailored, std_reads_00035_tailored = calculate_avg_std_given_a_list(list_sums_00035_tailored)
    avg_reads_00186_tailored, std_reads_00186_tailored = calculate_avg_std_given_a_list(list_sums_00186_tailored)

    avg_reads_00050_sld, std_reads_00050_sld = calculate_avg_std_given_a_list(list_sums_00050_sld)
    avg_reads_00035_sld, std_reads_00035_sld = calculate_avg_std_given_a_list(list_sums_00035_sld)
    avg_reads_00186_sld, std_reads_00186_sld = calculate_avg_std_given_a_list(list_sums_00186_sld)



    # print results in a nice form: mean \pm std
    print("Printing results...")
    print("")

    print("File 00050.root: NOAM, tailored, slidwind")
    print_mean_and_std(avg_reads_00050_NOAM, std_reads_00050_NOAM)
    print_mean_and_std(avg_reads_00050_tailored, std_reads_00050_tailored)
    print_mean_and_std(avg_reads_00050_sld, std_reads_00050_sld)
    print("")
    print("File 00035.root: NOAM, tailored, slidwind")
    print_mean_and_std(avg_reads_00035_NOAM, std_reads_00035_NOAM)
    print_mean_and_std(avg_reads_00035_tailored, std_reads_00035_tailored)
    print_mean_and_std(avg_reads_00035_sld, std_reads_00035_sld)
    print("")
    print("File 00186.root: NOAM, tailored, slidwind")
    print_mean_and_std(avg_reads_00186_NOAM, std_reads_00186_NOAM)
    print_mean_and_std(avg_reads_00186_tailored, std_reads_00186_tailored)
    print_mean_and_std(avg_reads_00186_sld, std_reads_00186_sld)
    print("")
    print("program finished!")



    #print("****  Generating reads results for LUSTRE has finished, check the file %s ... ****" %reads_results_lustre_file)
