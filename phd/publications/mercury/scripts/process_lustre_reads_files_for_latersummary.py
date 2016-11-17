__author__ = 'Federico G. Padua'


import os
import argparse


#lustre_dir_reads_server = 'lustre_reads_dir'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='This script generates preprocess LUSTRE reads traces, ready for averages and stds', version='0.0')
    parser.add_argument('-d', '--dir', help='Directory where LUSTRE read() OST or client traces are.', required=True)
    args = parser.parse_args()
    dir_LUSTRE_read_traces = args.dir
    lustre_dir_full_path = os.path.join(os.getcwd(), dir_LUSTRE_read_traces)
    list_of_trace_files = os.listdir(lustre_dir_full_path)

    for filename in list_of_trace_files:
        fin = open(os.path.join(lustre_dir_full_path, filename), "r")
        data_list = fin.readlines()
        fin.close()
        del data_list[0]
        del data_list[-1]
        # write the changed data (list) to a file
        fout = open(os.path.join(lustre_dir_full_path, filename), "w")
        fout.writelines(data_list)
        fout.close()
    print("****  Preprocessing of traces finished, please check them... ****")
