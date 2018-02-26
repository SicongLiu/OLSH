'''
Created on Feb 24, 2018

@author: sicongliu
'''

import math


def computer_qhull_statistics(data_file_path, k):
    num_of_data_elements_sum = 0
    for i in range(k):
        print 'Qhull Layer: ', str(i)
        data_file = data_file_path + str(i)
        f = open(data_file, 'r')
        lines = f.readlines()
        first_line = lines[0]
        metadata = first_line.split(" ")
        second_line = lines[1]
        num_of_data_elements = float(second_line.split('\n')[0])
        num_of_data_elements = int(num_of_data_elements)
        num_of_dimensions = float(metadata[0])
        num_of_dimensions = int(num_of_dimensions)

        num_of_data_elements_sum += num_of_data_elements

    # f = open(data_file_path, 'r')
    # lines = f.readlines()
    # first_line = lines[0]
    # metadata = first_line.split(" ")
    # second_line = lines[1]
    #
    # num_of_data_elements = float(second_line.split('\n')[0])
    # num_of_data_elements = int(num_of_data_elements)
    # num_of_dimensions = float(metadata[0])
    # num_of_dimensions = int(num_of_dimensions)
    # print 'Loading all data...'
    # data = []
    # for i in range(2, len(lines)):
    #     cur_line = lines[i]
    #     my_line = np.fromstring(cur_line, dtype=float, sep=' ')
    #     data.append(my_line)
    # qhull_list = {}
    #
    # # compute qhull iteratively
    # for i in range(k):
    #     command_line = command_bin_folder + '/qhull p < ' + data_file_path
    #     # execute command line through python
    #     output = os.popen(command_line).read()
    #     qhull_list[k] = output
    #     # save current qhull list to file
    #     save_current_qhull(output, i)
    #     data_file_path, data = save_remaining_qhull(num_of_data_elements, data, output, i)
    #     if num_of_data_elements - int(output.split('\n')[1]) >= num_of_dimensions + 1:
    #         continue
    #     else:
    #         break



if __name__ == '__main__':
    data_file_path = './qhull_layer_'
    k = 2
    computer_qhull_statistics(data_file_path, k)
    print 'Qhull Statistics Done'

