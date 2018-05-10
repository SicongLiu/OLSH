'''
Created on Feb 20, 2018

@author: sicongliu
'''

import numpy as np
import os


def save_current_qhull(current_qhull_list_output, layer, save_file_folder, aff_name):
    file_name = save_file_folder + '/' + aff_name + '_qhull_layer_' + str(layer)
    f = open(file_name, 'w')
    f.write(current_qhull_list_output)
    f.close()


def save_remaining_qhull(num_of_data_elements, data, current_qhull_output, layer_index, save_file_folder, aff_name):
    # remain_qhull_data = []
    remain_qhull = []
    current_data = current_qhull_output.split('\n')

    # process current_data
    # 1: dimension -- INTEGER
    # 2: number of points -- INTEGER
    # 3: point coordinates
    num_of_dimension = int(current_data[0])
    num_of_points = int(current_data[1])
    data_len = 2 + int(current_data[1])
    for i in range(2, data_len):
        current_data_record = np.fromstring(current_data[i], dtype=float, sep=' ')
        rows, columns = np.where(data == current_data_record)
        data.pop(rows[0])

        # print current_data_record
    file_name = save_file_folder + '/' + aff_name + '_remain_qhull_input_'+str(layer_index)
    remain_qhull.append(np.asarray(int(num_of_dimension)))
    remain_qhull.append(np.asarray(int(num_of_data_elements - num_of_points)))
    np.savetxt(file_name, remain_qhull, delimiter=',', fmt='%i')
    # separate metadata and data points, appending data points to metadata text saved on file
    f_handle = file(file_name, 'a')
    np.savetxt(f_handle, data)
    f_handle.close()
    return file_name, data


def computer_qhull_index(command_bin_folder, data_file_path, save_file_folder, aff_name, k):
    f = open(data_file_path, 'r')
    lines = f.readlines()
    first_line = lines[0]
    metadata = first_line.split(" ")
    second_line = lines[1]

    num_of_data_elements = float(second_line.split('\n')[0])
    num_of_data_elements = int(num_of_data_elements)
    num_of_dimensions = float(metadata[0])
    num_of_dimensions = int(num_of_dimensions)
    print 'Loading all data...'
    data = []
    for i in range(2, len(lines)):
        cur_line = lines[i]
        my_line = np.fromstring(cur_line, dtype=float, sep=' ')
        data.append(my_line)
    qhull_list = {}

    # compute qhull iteratively
    for i in range(k):
        command_line = command_bin_folder + '/qhull p < ' + data_file_path

        # execute command line through python
        output = os.popen(command_line).read()
        qhull_list[k] = output

        # save current qhull list to file
        save_current_qhull(output, i, save_file_folder, aff_name)
        data_file_path, data = save_remaining_qhull(num_of_data_elements, data, output, i, save_file_folder, aff_name)
        if num_of_data_elements - int(output.split('\n')[1]) >= num_of_dimensions + 1:
            num_of_data_elements = num_of_data_elements - int(output.split('\n')[1])
            continue
        else:
            break
    print 'testing program done'


if __name__ == '__main__':
    command_bin_folder = '/Users/sicongliu/Desktop/StreamingTopK/qhull/bin'

    # the top-k of interest
    k = 10
    file_count = 1
    my_save_file_folder = '/Users/sicongliu/Desktop/StreamingTopK/qhull/DATA/NBA'
    MY_AFF_NAME = 'nba_test'
    MY_DATA_FILE_PATH = '/Users/sicongliu/Desktop/StreamingTopK/qhull/DATA/NBA/NBA_2017_2018'

    my_aff_name = MY_AFF_NAME
    my_data_file_path = MY_DATA_FILE_PATH
    computer_qhull_index(command_bin_folder, my_data_file_path, my_save_file_folder, my_aff_name, k)

