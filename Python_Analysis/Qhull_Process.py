'''
Created on Feb 20, 2018

@author: sicongliu
'''

import numpy as np
import os


def save_current_qhull(current_qhull_list_output, layer, cur_output_folder, aff_name):
    file_name = cur_output_folder + '/' + aff_name + '_qhull_layer_' + str(layer)
    f = open(file_name, 'w')
    f.write(current_qhull_list_output)
    f.close()


def save_remaining_qhull(data_cardinality, data, current_qhull_output, layer_index, cur_output_folder, aff_name):
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

    file_name = cur_output_folder + '/' + aff_name + '_remain_qhull_input_'+str(layer_index)
    remain_qhull.append(np.asarray(int(num_of_dimension)))
    remain_qhull.append(np.asarray(int(data_cardinality - num_of_points)))
    np.savetxt(file_name, remain_qhull, delimiter=',', fmt='%i')

    # separate metadata and data points, appending data points to metadata text saved on file
    f_handle = file(file_name, 'a')
    np.savetxt(f_handle, data)
    f_handle.close()
    return file_name, data


def computer_qhull_index(command_bin_folder, input_path, output_folder, aff_name, max_layers):
    f = open(input_path, 'r')
    lines = f.readlines()
    first_line = lines[0]
    second_line = lines[1]

    cur_dimension = int(first_line.split('\n')[0])
    cur_cardinality = int(second_line.split('\n')[0])
    data = []
    for i in range(2, len(lines)):
        cur_line = lines[i]
        my_line = np.fromstring(cur_line, dtype=float, sep=' ')
        data.append(my_line)

    # compute qhull till max_layer of interest
    for i in range(max_layers):
        command_line = command_bin_folder + '/qhull p < ' + input_path
        output = os.popen(command_line).read()

        # flush current qhull list to file
        save_current_qhull(output, i, output_folder, aff_name)
        # save remaining points to file
        input_path, data = save_remaining_qhull(cur_cardinality, data, output, i, output_folder, aff_name)
        if cur_cardinality - int(output.split('\n')[1]) >= cur_dimension + 1:
            cur_cardinality = cur_cardinality - int(output.split('\n')[1])
            continue
        else:
            break


if __name__ == '__main__':
    command_bin_folder = '/Users/sliu104/Desktop/StreamingTopK/qhull/bin'
    dimensions = [2, 5, 7]
    # dimensions = [10, 15, 20]
    cardinality = [10000, 20000, 50000, 100000]

    data_type = ['anti_correlated_', 'correlated_', 'random_']
    # data_type = ['correlated_', 'random_']
    MAX_LAYERS = 10

    MY_DATA_FILE_PATH = '/Users/sliu104/Desktop/StreamingTopK/H2_ALSH/raw_data/Synthetic/'
    OUTPUT_PATH = '/Users/sliu104/Desktop/StreamingTopK/H2_ALSH/qhull_data/Synthetic'

    for i in range(len(dimensions)):
        for j in range(len(cardinality)):
            for k in range(len(data_type)):
                data_file_name = MY_DATA_FILE_PATH + data_type[k] + str(dimensions[i]) + "_" + str(cardinality[j]) + \
                                 ".txt"
                print("data name: " + data_file_name)
                my_aff_name = data_type[k] + str(dimensions[i]) + "_" + str(cardinality[j])
                computer_qhull_index(command_bin_folder, data_file_name, OUTPUT_PATH, my_aff_name, MAX_LAYERS)
