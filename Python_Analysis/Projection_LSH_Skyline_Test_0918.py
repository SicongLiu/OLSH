import os
import re
import sys
import numpy as np
import math
# import pandas as pd
# import matplotlib.pyplot as plt
from collections import Counter
import random



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

        # drop skyline points that are not supposed to be in the skyline list
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

    # cur_dimension = int(first_line.split('\n')[0])
    cur_dimension = 2
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
        output, output_cardinality, remain_data, remain_cardinality = find_skyline_bnl(data, cur_dimension, cur_cardinality)

        # flush current qhull list to file
        save_current_qhull(output, i, output_folder, aff_name, cur_dimension, output_cardinality)
        # save remaining points to file

        # update data
        data = remain_data
        cur_cardinality = remain_cardinality

        if remain_cardinality < cur_dimension + 1:
            break


def select_dim(nums_, min_, max_):
    dim_list_ = []
    for x in range(nums_):
        dim_list_.append(random.randint(min_, max_))
    return dim_list_


def dot(K, L):
    if len(K) != len(L):
        return 0
    return float("{0:.5f}".format(sum(i[0] * i[1] for i in zip(K, L))))


def compute_ground_truth(query_list_, data_list_, top_k_):
    grountTruth_ = []
    for ii in range(query_list_.__len__()):
        dot_val_list_ = []
        for jj in range(query_list_.__len__()):
            dot_val_list_.append(dot(query_list_[ii], data_list_[jj]))  # dot product value, the larger the better
        temp_grountTruth_ = np.argsort(dot_val_list_)[::-1]
        temp_grountTruth_ = temp_grountTruth_[0:top_k_]
        grountTruth_.append(temp_grountTruth_)
    return grountTruth_


def angle(data_, norm_data_, query_, norm_query_):
    return math.acos(1.0 * dot(data_, query_) / (norm_data_ * norm_query_))


def compute_recall(grountTruth_, ret_index_):
    intersection = len(list(set(grountTruth_).intersection(set(ret_index_))))
    return float(1.0 * intersection / len(grountTruth_))


def transform_query(query_, query_norm_, pivot_, pivot_norm_):
    alpha_ = angle(query_, query_norm_, pivot_, pivot_norm_)
    tuple_ = []
    # convert minus to plus
    # t1_ = (math.sin(alpha_) * math.sin(alpha_) - 1)/(2 * math.cos(alpha_))
    t1_ = (-1.0) * (math.sin(alpha_) * math.sin(alpha_) - 1) / (2 * math.cos(alpha_))
    t2_ = math.cos(alpha_)
    tuple_.append(t1_)
    tuple_.append(t2_)
    return tuple_


def transform_data(data_, data_norm_, pivot_, pivot_norm_):
    beta_ = angle(data_, data_norm_, pivot_, pivot_norm_)
    tuple_ =[]
    # convert minus to plus
    # t1_ = (-1.0) * data_norm_ * math.cos(beta_)
    t1_ = data_norm_ * math.cos(beta_)
    t2_ = (-1.0) * data_norm_ * (math.sin(beta_) * math.sin(beta_) - 1) / (2 * math.cos(beta_))
    # t1_ = data_norm_ * math.cos(beta_)
    # t2_ = data_norm_ * (math.sin(beta_) * math.sin(beta_) - 1) / (2 * math.cos(beta_))
    tuple_.append(t1_)
    tuple_.append(t2_)
    return tuple_


def load_data(data_file):
    # load data
    f = open(data_file, 'r')
    lines = f.readlines()
    cur_dim = int(lines[0])
    cur_card = int(lines[1])
    data_list = []
    data_norm_list = []
    for i in range(cur_card):
        current_data_record = np.fromstring(lines[i + 2], dtype=float, sep=' ')
        current_data_record = np.asarray(current_data_record)
        temp_norm = np.linalg.norm(current_data_record)
        data_norm_list.append(float("{0:.5f}".format(temp_norm)))
        data_list.append(current_data_record)
    f.close()
    return data_list, data_norm_list


def load_query(query_file):
    # load query
    f = open(query_file, 'r')
    lines = f.readlines()

    cur_dim = int(lines[0])
    cur_card = int(lines[1])
    query_list = []
    query_norm_list = []
    for i in range(cur_card):
        current_data_record = np.fromstring(lines[i + 2], dtype=float, sep=' ')
        current_data_record = np.asarray(current_data_record)
        # compute ground truth
        query_list.append(current_data_record)
        temp_norm = np.linalg.norm(current_data_record)
        # data_norm_list.append(format(temp_norm, '.5f'))
        query_norm_list.append(float("{0:.5f}".format(temp_norm)))
    f.close()
    return query_list, query_norm_list


def save_transformed_data(data_type_, selected_index_, cardinality_, transform_list_):
    raw_data_ = []
    file_name_ = data_type_ + "_" + str(selected_index_) + "_" + str(cardinality_) + ".txt"
    raw_data_.append(np.asarray(int(pivot_index)))
    raw_data_.append(np.asarray(int(cardinality)))
    raw_data_ = np.asarray(raw_data_)
    np.savetxt(file_name_, raw_data_, delimiter=',', fmt='%i')

    # separate metadata and data points, appending data points to metadata text saved on file
    f_handle = open(file_name_, 'ab')
    np.savetxt(f_handle, transform_list_, fmt='%10.6f')
    f_handle.close()


def save_transformed_query(data_type_, selected_index_, cardinality_, transform_list_):
    raw_data_ = []
    file_name_ = data_type_ + "_" + str(selected_index_) + "_" + str(cardinality_) + ".txt"
    raw_data_.append(np.asarray(int(pivot_index)))
    raw_data_.append(np.asarray(int(cardinality)))
    raw_data_ = np.asarray(raw_data_)
    np.savetxt(file_name_, raw_data_, delimiter=',', fmt='%i')

    # separate metadata and data points, appending data points to metadata text saved on file
    f_handle = open(file_name_, 'ab')
    np.savetxt(f_handle, transform_list_, fmt='%10.6f')
    f_handle.close()


def save_transformed_query(query_type_, selected_index_, transform_query_):
    raw_data_ = []
    file_name_ = query_type_ + "_" + str(selected_index_) + ".txt"
    raw_data_.append(np.asarray(int(pivot_index)))
    raw_data_.append(np.asarray(int(cardinality)))
    raw_data_ = np.asarray(raw_data_)
    np.savetxt(file_name_, raw_data_, delimiter=',', fmt='%i')

    # separate metadata and data points, appending data points to metadata text saved on file
    f_handle = open(file_name_, 'ab')
    np.savetxt(f_handle, transform_query_, fmt='%10.6f')
    f_handle.close()


def load_transformed_query(query_file_name_):
    f = open(query_file_name_, 'r')
    lines = f.readlines()
    cur_dim = int(lines[0])
    cur_card = int(lines[1])
    data_list = []
    for i in range(cur_card):
        current_data_record = np.fromstring(lines[i + 2], dtype=float, sep=' ')
        current_data_record = np.asarray(current_data_record)
        data_list.append(current_data_record)
    f.close()
    return data_list


def save_ground_truth(ground_truth_file_, ground_truth_):
    f_handle = open(ground_truth_file_, 'ab')
    # np.savetxt(f_handle, ground_truth_, fmt='%10.6f')
    np.savetxt(f_handle, ground_truth_, fmt='%i')
    f_handle.close()


dimension = 100
cardinality = 100000
data_type = 'random'
query_type = '2D'
data_file = './' + data_type + "_" + str(dimension) + '_' + str(cardinality) + '.txt'
query_file = 'query_' + str(dimension) + 'D' + '.txt'
data_list, data_norm_list = load_data(data_file)
query_list, query_norm_list = load_query(query_file)

# compute and rank results based on theta_min = beta - alpha
top_k = 25
# ground_truth = compute_ground_truth(query_list, data_list, top_k)
# ground_truth_file = "./ground_truth.txt"
# save_ground_truth(ground_truth_file, ground_truth)

# compute and rank results based on theta_min = beta - alpha
projected_dim = 2
top_k = 25
min_ = 0
max_ = dimension - 1
total_round = 1 # for each list of dims, selected round to deal with randomness

nums_ = 25
dim_list = select_dim(nums_, min_, max_)
# dim_list = [57]
for jj in range(nums_):
    print("Current round: " + str(jj) + ", Current dims: " + str(nums_) + " dimension chosen: " + str(dim_list))
    transform_list = []
    theta_list = []
    pivot = np.zeros(dimension)
    pivot_index = dim_list[jj]
    pivot[pivot_index] = 1
    pivot_norm = 1
    for kk in range(data_list.__len__()):
        tuple_data = transform_data(data_list[kk], data_norm_list[kk], pivot, pivot_norm)
        transform_list.append(tuple_data)
    transform_list = np.asarray(transform_list)

    save_transformed_data(data_type, pivot_index, cardinality, transform_list)
    # query transformed based on this dimension
    total_transformed_query = []
    for ii in range(query_list.__len__()):
        tuple_query = transform_query(query_list[ii], query_norm_list[ii], pivot, pivot_norm)
        total_transformed_query.append(tuple_query)
    save_transformed_query(query_type, pivot_index, total_transformed_query)


print('Transformed data and query saved')
# # compute Skyline


# # query using skyline
# skyline_folder = "./"
# query_folder = "./"
#
# for jj in nums_:
#     pivot_index = dim_list[jj]
#     transformed_query_file = query_folder + query_type + "_" + str(pivot_index) + '.txt'
#     # load query
#     transform_query_list = load_transformed_query(transformed_query_file)
#     for kk in range(top_k):
#         skyline_file = skyline_folder + data_type + "_" + str(pivot_index) + "_" + str(cardinality) + "_qhull_layer_" + str(kk)
#         # load transformed_data via skyline layer
#         transformed_skyline_data = load_transformed_query(skyline_file)
#
#         # query top-(top_k - kk)
#
#     # aggregate result and compute recall










# dimensions = [57]
# cardinality = [100000]
# data_type = ['random']
# dim_selected = 57
# MAX_LAYERS = top_k
#
# # MY_DATA_FILE_PATH = '/Users/sicongliu/Desktop/StreamingTopK/H2_ALSH/raw_data/Synthetic/'
# MY_DATA_FILE_PATH = './'
# OUTPUT_PATH = '/Users/sliu104/Desktop/StreamingTopK/H2_ALSH/qhull_data/Synthetic_test'
#
# for i in range(len(dimensions)):
#     for j in range(len(cardinality)):
#         for k in range(len(data_type)):
#             data_file_name = MY_DATA_FILE_PATH + data_type[k] + "_" + str(dim_selected) + "_"+ str(cardinality[j]) + ".txt"
#             # data_file_name = MY_DATA_FILE_PATH + data_type[k] + "_" + str(cardinality[j]) + \
#             #                  ".txt"
#             print("data name: " + data_file_name)
#             my_aff_name = data_type[k] + str(dimensions[i]) + "_" + str(cardinality[j])
#             computer_qhull_index(data_file_name, OUTPUT_PATH, my_aff_name, MAX_LAYERS)

# query



print('Done')