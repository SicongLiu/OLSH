'''
Created on August 15, 2019

@author: sicongliu
'''

import numpy as np


'''run skyline query k-times'''
# check if pointA domniates pointB
def IsADominateB(PointA, PointB, dim_):
    n_better = 0
    for d_ in range(dim_):
        if PointA[d_] < PointB[d_]:
            return False
        n_better += PointA[d_] > PointB[d_]

    if n_better > 0:
        return True
    return False


def count_diffs(a, b, dim_):
    n_better = 0
    n_worse = 0

    for f in range(dim_):
        n_better += a[f] > b[f]
        n_worse += a[f] < b[f]

    return n_better, n_worse


def find_skyline_bnl(data_, dim_, card_):
    """Finds the skyline using a block-nested loop."""

    # Use the first row to initialize the skyline
    skyline = {0}
    total_index = range(len(data_))
    total_index = set(total_index)
    # Loop through the rest of the rows
    for i in range(1, card_):

        to_drop = set()
        is_dominated = False

        for j in skyline:

            n_better, n_worse = count_diffs(data_[i, :], data_[j, :], dim_)

            # Case 1: pointA is dominated by pointB, discard pointA
            if n_worse > 0 and n_better == 0:
                is_dominated = True
                break

            # Case 3: if this point dominates any poin in the list,, insert this point and the dominated point in the list is discarded
            if n_better > 0 and n_worse == 0:
                to_drop.add(j)

        # if point is neither dominated-by or dominates other points, insert it without dropping points
        if is_dominated:
            continue

        skyline = skyline.difference(to_drop)
        skyline.add(i)

    skyline_list = list(skyline)
    skyline_data_ = data_[skyline_list, :]
    skyline_cardinality = len(skyline_data_)
    remain_data_index = list(total_index.difference(skyline))
    remain_data_ = data_[remain_data_index, :]
    remain_card_ = card_ - len(skyline_data_)
    return skyline_data_, skyline_cardinality, remain_data_, remain_card_


def save_current_qhull(current_qhull_list_output, layer, cur_output_folder, aff_name, dim_, card_):
    file_name = cur_output_folder + '/' + aff_name + '_qhull_layer_' + str(layer)
    # f = open(file_name, 'w')
    # f.write(dim_)
    # f.write(card_)
    # f.write(current_qhull_list_output)
    # f.close()
    data_to_be_save = []
    data_to_be_save.append(np.asarray(int(dim_)))
    data_to_be_save.append(np.asarray(int(card_)))
    data_to_be_save = np.asarray(data_to_be_save)
    np.savetxt(file_name, data_to_be_save, delimiter=',', fmt='%i')

    # separate metadata and data points, appending data points to metadata text saved on file
    f_handle = open(file_name, 'ab')
    np.savetxt(f_handle, current_qhull_list_output, fmt='%10.6f')
    f_handle.close()
    # return file_name, data





def save_remaining_qhull(data_cardinality, data, current_qhull_output, layer_index, cur_output_folder, aff_name):
    remain_qhull = []
    current_data = current_qhull_output.split('\n')

    # 1st line: dimension -- INTEGER
    # 2nd line: number of points -- INTEGER
    # 3: point coordinates
    current_data = np.asarray(current_data)
    num_of_dimension = int(current_data[0])
    num_of_points = int(current_data[1])
    data_len = 2 + int(current_data[1])
    for i in range(2, data_len):
        current_data_record = np.fromstring(current_data[i], dtype=float, sep=' ')
        # rows, columns = np.where((data == current_data_record).all(axis=1))
        my_row = np.where((data == current_data_record).all(axis=1))[0]
        data = np.delete(data, my_row, 0)

    file_name = cur_output_folder + '/' + aff_name + '_remain_qhull_input_'+str(layer_index)
    remain_qhull.append(np.asarray(int(num_of_dimension)))
    remain_qhull.append(np.asarray(int(data_cardinality - num_of_points)))
    remain_qhull = np.asarray(remain_qhull)
    np.savetxt(file_name, remain_qhull, delimiter=',', fmt='%i')

    # separate metadata and data points, appending data points to metadata text saved on file
    f_handle = open(file_name, 'ab')
    np.savetxt(f_handle, data, fmt='%10.6f')
    f_handle.close()
    return file_name, data


def computer_qhull_index(input_path, output_folder, aff_name, max_layers):
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

    data = np.asarray(data)
    print(type(data))
    # compute qhull till max_layer of interest
    for i in range(max_layers):
        # command_line = command_bin_folder + '/qhull p < ' + input_path
        # output = os.popen(command_line).read()
        output, output_cardinality, remain_data, remain_cardinality = find_skyline_bnl(data, cur_dimension, cur_cardinality)

        # flush current qhull list to file
        save_current_qhull(output, i, output_folder, aff_name, cur_dimension, output_cardinality)
        # save remaining points to file
        # input_path, data = save_remaining_qhull(cur_cardinality, data, output, i, output_folder, aff_name)

        # update data
        data = remain_data
        cur_cardinality = remain_cardinality

        if remain_cardinality < cur_dimension + 1:
            break

        # if cur_cardinality - int(output.split('\n')[1]) >= cur_dimension + 1:
        #     cur_cardinality = cur_cardinality - int(output.split('\n')[1])
        #     continue
        # else:
        #     break


if __name__ == '__main__':
    dimensions = [4]
    # dimensions = [10, 15, 20]
    cardinality = [100]
    # data_type = ['anti_correlated_', 'correlated_', 'random_']
    data_type = ['anti_correlated_']
    MAX_LAYERS = 2

    MY_DATA_FILE_PATH = '/Users/sicongliu/Desktop/StreamingTopK/H2_ALSH/raw_data/Synthetic/'
    OUTPUT_PATH = '/Users/sicongliu/Desktop/StreamingTopK/H2_ALSH/qhull_data/Synthetic_test'
    # MY_DATA_FILE_PATH = '/Users/sicongliu/Desktop/StreamingTopK/H2_ALSH/raw_data/Synthetic/'
    # OUTPUT_PATH = '/Users/sicongliu/Desktop/StreamingTopK/H2_ALSH/qhull_data/Synthetic_test'
    # OUTPUT_PATH = '/Users/sicongliu/StreamingTopK/H2_ALSH/qhull_data/Synthetic_test'

    for i in range(len(dimensions)):
        for j in range(len(cardinality)):
            for k in range(len(data_type)):
                data_file_name = MY_DATA_FILE_PATH + data_type[k] + str(dimensions[i]) + "_" + str(cardinality[j]) + \
                                 ".txt"
                print("data name: " + data_file_name)
                my_aff_name = data_type[k] + str(dimensions[i]) + "_" + str(cardinality[j])
                computer_qhull_index(data_file_name, OUTPUT_PATH, my_aff_name, MAX_LAYERS)
