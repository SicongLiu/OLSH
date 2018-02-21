'''
Created on Feb 20, 2018

@author: sicongliu
'''

import subprocess as sb


def computer_qhull_index(command_bin_folder, data_file_path, k):
    # load data

    command_line = command_bin_folder + '/qhull'
    # compute qhull iteratively
    for i in range(k):

    print 'testing program done'


if __name__ == '__main__':
    command_bin_folder = '/Users/sliu104/Desktop/StreamingTopK/qhull-2015.2/bin'
    data_file_path = '/Users/sliu104/Desktop/StreamingTopK/qhull-2015.2/bin/data_sample/data_ICDE_2010'
    k = 3
    computer_qhull_index(command_bin_folder, data_file_path, k)
    output = sb.check_output(['ls', '-l'])
    print output
