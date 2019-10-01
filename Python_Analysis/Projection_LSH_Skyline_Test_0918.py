import os
import re
import sys
import numpy as np
import math
# import pandas as pd
# import matplotlib.pyplot as plt
from collections import Counter
import random
import json


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
    # current_list = [0, 1, 4, 6, 7, 8, 11, 14, 16, 17, 18, 19, 21, 22, 26, 28, 31, 33, 34, 35, 36, 37, 40, 42, 45, 47, 50, 51, 52, 54, 55, 57, 59, 60, 63, 65, 69, 71, 75, 81, 82, 87, 89, 91, 92, 93, 94, 96, 98, 99]
    current_list = [0, 1, 4, 6, 7, 8, 11, 14, 16, 17, 18, 19, 21, 22, 26, 28, 31, 33, 34, 35, 36, 37, 40, 42, 45, 47, 50, 51, 52, 54, 55, 57, 59, 60, 63, 65, 69, 71, 75, 81, 82, 87, 89, 91, 92, 93, 94, 96, 98, 99, 3, 9, 10, 13, 15, 23, 25, 29, 30, 38, 39, 46, 48, 49, 53, 58, 61, 62, 68, 72, 73, 76, 79, 83, 88, 66, 5, 70, 41, 74, 80, 85, 86, 90, 95]

    temp_list_ = set(current_list)
    dim_list_ = set()
    for x in range(nums_):
        xx = random.randint(min_, max_)
        while temp_list_.__contains__(xx):
            xx = random.randint(min_, max_)
        dim_list_.add(xx)
        temp_list_.add(xx)
    return list(dim_list_), list(temp_list_)


def dot_update(K, L):
    # if len(K) != len(L):
    #     return 0
    L = L[0: 2]
    if len(K) != len(L):
        return 0
    return float("{0:.5f}".format(sum(i[0] * i[1] for i in zip(K, L))))


def dot(K, L):
    if len(K) != len(L):
        return 0
    return float("{0:.5f}".format(sum(i[0] * i[1] for i in zip(K, L))))

def compute_ground_truth(query_list_, data_list_, top_k_):
    grountTruth_ = []
    for ii in range(query_list_.__len__()):
        dot_val_list_ = []
        for jj in range(data_list_.__len__()):
            dot_val_list_.append(dot(query_list_[ii], data_list_[jj]))  # dot product value, the larger the better
        temp_grountTruth_ = np.argsort(dot_val_list_)[::-1]
        temp_grountTruth_ = temp_grountTruth_[0:top_k_]
        grountTruth_.append(temp_grountTruth_)
    return grountTruth_


def angle(data_, norm_data_, query_, norm_query_):
    return math.acos(1.0 * dot(data_, query_) / (norm_data_ * norm_query_))


def compute_recall(grountTruth_, ret_index_, top_k_):
    temp_ground_truth = take_ground_truth(grountTruth_, top_k_)
    intersection = len(list(set(temp_ground_truth).intersection(set(ret_index_))))
    return float(1.0 * intersection / len(temp_ground_truth))


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
    raw_data_.append(np.asarray(int(selected_index_)))
    raw_data_.append(np.asarray(int(cardinality)))
    raw_data_ = np.asarray(raw_data_)
    np.savetxt(file_name_, raw_data_, delimiter=',', fmt='%i')

    # separate metadata and data points, appending data points to metadata text saved on file
    f_handle = open(file_name_, 'ab')
    np.savetxt(f_handle, transform_list_, fmt='%10.6f')
    f_handle.close()


def save_transformed_data(data_type_, selected_index_, cardinality_, transform_list_):
    raw_data_ = []
    file_name_ = data_type_ + "_" + str(selected_index_) + "_" + str(cardinality_) + ".txt"
    raw_data_.append(np.asarray(int(selected_index_)))
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
    raw_data_.append(np.asarray(int(selected_index_)))
    raw_data_.append(np.asarray(int(cardinality)))
    raw_data_ = np.asarray(raw_data_)
    np.savetxt(file_name_, raw_data_, delimiter=',', fmt='%i')

    # separate metadata and data points, appending data points to metadata text saved on file
    f_handle = open(file_name_, 'ab')
    np.savetxt(f_handle, transform_query_, fmt='%10.6f')
    f_handle.close()


def load_transformed_query(query_file_name_, query_size_):
    f = open(query_file_name_, 'r')
    lines = f.readlines()
    cur_dim = int(lines[0])
    cur_card = int(lines[1])
    data_list = []
    for i in range(query_size_):
        current_data_record = np.fromstring(lines[i + 2], dtype=float, sep=' ')
        current_data_record = np.asarray(current_data_record)
        data_list.append(current_data_record)
    f.close()
    return data_list, query_size_


def load_transformed_data(query_file_name_, query_size_):
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
    return data_list, cur_card

def save_ground_truth(ground_truth_file_, ground_truth_):
    f_handle = open(ground_truth_file_, 'ab')
    # np.savetxt(f_handle, ground_truth_, fmt='%10.6f')
    np.savetxt(f_handle, ground_truth_, fmt='%i')
    f_handle.close()


def load_ground_truth(ground_truth_file_, card_):
    f = open(ground_truth_file_, 'r')
    lines = f.readlines()
    data_list = []
    for i in range(card_):
        current_data_record = np.fromstring(lines[i], dtype=float, sep=' ')
        current_data_record = np.asarray(current_data_record)
        data_list.append(current_data_record)
    f.close()
    return data_list


def load_into_dict(my_dict_, data_index_list_, val_list_, query_index_):
    temp_dict = {}
    if my_dict_.__contains__(query_index_):
        temp_dict = my_dict_[query_index_]
    else:
        temp_dict = {}
    for dd in range(data_index_list_.__len__()):
        if temp_dict.__contains__(data_index_list_[dd]):
            temp_dict[data_index_list_[dd]] = data_index_list_[dd] + val_list_[dd]
        else:
            temp_dict[data_index_list_[dd]] = val_list_[dd]
    my_dict_[query_index_] = temp_dict
    return my_dict_


def save_dict_to_file(my_dict_, raw_query_list_, raw_data_list_):
    # save global dict to file
    file_name_ = "./global_val_dict.txt"
    f_handle = open(file_name_, 'ab')
    for dd in my_dict_.keys():
        sorted_x = sorted(my_dict_[dd].items(), key=lambda kv: kv[1], reverse=True)
        temp_dict = score_aggregation(sorted_x[0: 50], raw_query_list_[dd], raw_data_list_)
        # f_handle.write(str(sorted_x[0: 50]))
        f_handle.write(str(temp_dict))
        f_handle.write("\n")
    f_handle.close()


def score_aggregation(key_val_list_, raw_query_, raw_data_list_):
    temp_dict_ = {}
    for ii in range(len(key_val_list_)):
        id_ = int(key_val_list_[ii][0])
        temp_dict_[id_] = dot(raw_query_, raw_data_list_[id_])
    return temp_dict_


def take_ground_truth(temp, top_k):
    ret = []
    for ii in range(top_k):
        ret.append(temp[2 * ii])
    return ret


def histedges_equalN(x, nbin):
    npt = len(x)
    return np.interp(np.linspace(0, npt, nbin + 1),
                     np.arange(npt),
                     np.sort(x))


def norm_partition(data_list_, data_norm_list_, bin_count_, data_type_, dimension_, cardinality_):
    # partition based on norm of data
    norm_min = min(data_norm_list_)
    norm_max = max(data_norm_list_)

    bin_edge = histedges_equalN(data_norm_list_, bin_count_)
    digitize_index_ = np.digitize(data_list_, bin_edge)

    # bin_aggregate, bin_edge = np.histogram(data_norm_list_, bins=bin_count_)
    # digitize_index_ = np.digitize(data_norm_list_, bin_edge)
    # save each partition to file
    for bb in range(bin_count_):
        temp_batch = []
        temp_batch.append(np.asarray(int(dimension_)))
        data_index_ = np.where(digitize_index_ == bb + 1)  # those data save as bb
        temp_batch.append(np.asarray(int(data_index_.__len__())))
        current_file = "./" + data_type_ + "_" + str(dimension_) + "_" + str(cardinality) + "_" + str(bb) + ".txt"
        temp_batch = np.asarray(temp_batch)
        np.savetxt(current_file, temp_batch, delimiter=',', fmt='%i')

        temp_batch = []

        for dd in range(data_index_.__len__()):
            temp_batch.append(data_list_[dd])
        # separate metadata and data points, appending data points to metadata text saved on file
        f_handle = open(current_file, 'ab')
        np.savetxt(f_handle, temp_batch, fmt='%10.6f')
        f_handle.close()




dimension = 100
cardinality = 100000
data_type = 'random'
query_type = '2D'
data_file = './' + data_type + "_" + str(dimension) + '_' + str(cardinality) + '.txt'
query_file = 'query_' + str(dimension) + 'D' + '.txt'
data_list, data_norm_list = load_data(data_file)
query_list, query_norm_list = load_query(query_file)

bin_count = 10
norm_partition(data_list, data_norm_list, bin_count, data_type, dimension, cardinality)



top_k = 25

# compute and rank results based on theta_min = beta - alpha
# ground_truth = compute_ground_truth(query_list, data_list, top_k)
ground_truth_file = "./ground_truth_1000.txt"
# save_ground_truth(ground_truth_file, ground_truth)

# compute and rank results based on theta_min = beta - alpha
projected_dim = 2
query_size = 100

min_ = 0
max_ = dimension - 1
total_round = 1 # for each list of dims, selected round to deal with randomness

nums_ = 100
# dim_list, total_list = select_dim(nums_, min_, max_)
# dim_list = [17, 80, 26, 88, 90, 96, 57, 76, 70, 55, 54, 57, 61, 11, 38, 53, 94, 94, 92, 21, 23, 3, 45, 73, 41]
# dim_list = [0, 1, 4, 6, 7, 8, 11, 14, 16, 17, 18, 19, 21, 22, 26, 28, 31, 33, 34, 35, 36, 37, 40, 42, 45, 47, 50, 51, 52, 54, 55, 57, 59, 60, 63, 65, 69, 71, 75, 81, 82, 87, 89, 91, 92, 93, 94, 96, 98, 99]
# dim_list = [0, 1, 4, 6, 7, 8, 11, 14, 16, 17, 18, 19, 21, 22, 26, 28, 31, 33, 34, 35, 36, 37, 40, 42, 45, 47, 50, 51, 52, 54, 55, 57, 59, 60, 63, 65, 69, 71, 75, 81, 82, 87, 89, 91, 92, 93, 94, 96, 98, 99, 3, 9, 10, 13, 15, 23, 25, 29, 30, 38, 39, 46, 48, 49, 53, 58, 61, 62, 68, 72, 73, 76, 79, 83, 88]
# dim_list = [0, 1, 4, 6, 7, 8, 11, 14, 16, 17, 18, 19, 21, 22, 26, 28, 31, 33, 34, 35, 36, 37, 40, 42, 45, 47, 50, 51, 52, 54, 55, 57, 59, 60, 63, 65, 69, 71, 75, 81, 82, 87, 89, 91, 92, 93, 94, 96, 98, 99, 3, 9, 10, 13, 15, 23, 25, 29, 30, 38, 39, 46, 48, 49, 53, 58, 61, 62, 68, 72, 73, 76, 79, 83, 88, 66, 5, 70, 41, 74, 80, 85, 86, 90, 95]
dim_list = [0, 1, 4, 6, 7, 8, 11, 14, 16, 17, 18, 19, 21, 22, 26, 28, 31, 33, 34, 35, 36, 37, 40, 42, 45, 47, 50, 51, 52, 54, 55, 57, 59, 60, 63, 65, 69, 71, 75, 81, 82, 87, 89, 91, 92, 93, 94, 96, 98, 99, 3, 9, 10, 13, 15, 23, 25, 29, 30, 38, 39, 46, 48, 49, 53, 58, 61, 62, 68, 72, 73, 76, 79, 83, 88, 66, 5, 70, 41, 74, 80, 85, 86, 90, 95, 32, 97, 2, 67, 64, 44, 43, 12, 77, 78, 56, 20, 24, 84, 27]
# dim_list = [0, 1, 4, 6, 7, 8, 11, 14, 16, 17]

print(set(dim_list).__len__())
# print(set(total_list).__len__())
for bb in range(bin_count):
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
# # compute Skyline, using C++ script

# now do query
#  at j-th layers, select top-(k - j + 1)
# use dict{} to store results for each query
skyline_folder = "/Users/sliu104/Desktop/StreamingTopK/H2_ALSH/qhull_data/Synthetic_test/"
global_result = {}
ground_truth = load_ground_truth(ground_truth_file, query_size)
global_value_dict = {}# key: query id. value: dict.
for ii in range(nums_):
    cur_dim = dim_list[ii] # projected dimension
    local_query_file = '2D_' + str(cur_dim) + '.txt'
    local_trans_query, query_size = load_transformed_query(local_query_file, query_size) # locate query file


    for kk in range(top_k):
        local_data_file = skyline_folder + data_type + "_" + str(cur_dim) + "_" + str(cardinality) + "_qhull_layer_" + str(kk)
        local_trans_data, data_size = load_transformed_data(local_data_file, query_size) # locate top-k data file

        for jj in range(query_size): # for each query compute top-k, use map for cache
            temp_dot_val = []
            for tt in range(local_trans_data.__len__()):
                temp_dot_val.append(dot_update(local_trans_query[jj], local_trans_data[tt]))
            local_trans_data = np.asarray(local_trans_data)



            # save_dict_to_file(global_value_dict)

            min_length = min(top_k - kk, data_size)

            temp_index = np.argsort(temp_dot_val)[::-1][0: min_length]
            # local_result.extend(local_trans_data[temp_index, 2])
            local_result = local_trans_data[temp_index, 2]
            # global_value_dict = load_into_dict(global_value_dict, local_trans_data[:, 2], temp_dot_val, jj)
            global_value_dict = load_into_dict(global_value_dict, local_result, temp_dot_val, jj)
            if jj in global_result.keys():
                global_result[jj] = np.asarray(np.concatenate((global_result[jj], local_result), axis=None))
            else:
                global_result[jj] = local_result
    # temp_dict = global_value_dict[0]
    # print(temp_dict)
    # print(len(temp_dict))

recall_list_transform = []
for ii in global_result.keys():
    global_result[ii] = list(set(global_result[ii]))
    recall_val = compute_recall(ground_truth[ii], global_result[ii], top_k)
    print("Current key: " + str(ii) + ", current recall_val: " + str(recall_val))
    # recall_list_transform.append(compute_recall(grountTruth[ii], transform_list_ground_truth))
    recall_list_transform.append(recall_val)

save_dict_to_file(global_value_dict, query_list, data_list)
print("current selected dim:  " + str(nums_) + " --  " + str(1.0 * sum(recall_list_transform) / recall_list_transform.__len__()))

# for jj in range(query_size):
#     local_result = []
#     temp_dot_val = []
#     for kk in range(top_k):
#         local_data_file = data_type + "_" + str(cur_dim) + "_" + str(cardinality) + "_" + str(kk) +".txt"
#         local_trans_data, data_size = load_transformed_query(local_data_file)
#         for tt in range(local_trans_data.__len__()):
#             temp_dot_val.append(dot(local_trans_query[jj], local_trans_data[tt]))
#         local_trans_data = np.asarray(local_trans_data)
#         temp_index = np.argsort(temp_dot_val)[::-1][0: top_k - kk + 1]
#         local_result.extend(local_trans_data[temp_index, 2])
#     local_result = set(local_result)
#     local_result = list(local_result)
#
#     if jj in global_result.keys():
#         global_result[jj].extend(local_result)
#     else:
#         global_result[jj] = local_result
#     # recall_val = compute_recall(ground_truth[jj], local_result)
#     # recall_list_transform.append(recall_val)



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