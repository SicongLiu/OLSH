import os
import re
import sys
from openpyxl import load_workbook
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import math
from scipy.stats import beta


def load_query(query_folder_, dimension_):
    query_file_name = query_folder_ + 'query_' + str(dimension_) + 'D.txt'
    f = open(query_file_name, 'r')
    lines = f.readlines()
    cur_dim = int(lines[0])
    cur_card = int(lines[1])
    query_list = []
    for kk in range(cur_card):
        current_query_record = np.fromstring(lines[kk + 2], dtype=float, sep=' ')
        current_query_record = np.asarray(current_query_record)
        query_list.append(current_query_record)
    f.close()
    return np.asarray(query_list)


def compute_alpha_beta(input_ndarray_, min_index_, max_index_):
    sample_mean = np.mean(input_ndarray_)
    sample_var = np.var(input_ndarray_, ddof=1)
    x_bar = float(sample_mean - min_index_) / float(max_index_ - min_index_)
    var_bar = float(sample_var) / math.pow(float(max_index_ - min_index_), 2)
    alpha_ = x_bar * (x_bar * (1 - x_bar)/var_bar - 1)
    beta_ = (1 - x_bar) * (x_bar * (1 - x_bar)/var_bar - 1)

    return alpha_, beta_


def compute_norm(input_file_, dimension_, card_):
    f = open(input_file_, 'r')
    lines = f.readlines()

    cur_dim = int(lines[0])
    cur_card = int(lines[1])

    assert cur_dim == dimension_
    assert cur_card == card_

    data_norm_list = []
    data_list = []
    for kk in range(cur_card):
        current_data_record = np.fromstring(lines[kk + 2], dtype=float, sep=' ')
        current_data_record = np.asarray(current_data_record)
        data_list.append(current_data_record)
        # temp_norm = float(format(np.linalg.norm(current_data_record), '.7f'))
        temp_norm = np.linalg.norm(current_data_record)
        data_norm_list.append(temp_norm)
    f.close()
    data_norm_list = np.asarray(data_norm_list)
    data_list = np.asarray(data_list)

    return data_norm_list, data_list


def save_bin_partition_on_file(bin_count_, data_type_, dimension_, card_, digitize_index_, data_list):
    for bb in range(bin_count_):
        temp_batch = []
        temp_batch.append(np.asarray(int(dimension_)))
        data_index_ = np.where(digitize_index_ == bb + 1)  # those data save as bb
        temp_batch.append(np.asarray(int(data_index_.__len__())))

        current_file = "./" + data_type_ + "_" + str(dimension_) + "_" + str(card_) + "_" + str(bb) + ".txt"
        temp_batch = np.asarray(temp_batch)
        np.savetxt(current_file, temp_batch, delimiter=',', fmt='%i')

        temp_batch = []

        for dd in range(data_index_.__len__()):
            temp_batch.append(data_list[dd])
        # separate metadata and data points, appending data points to metadata text saved on file
        f_handle = open(current_file, 'ab')
        np.savetxt(f_handle, temp_batch, fmt='%10.6f')
        f_handle.close()


def dot(K, L):
   if len(K) != len(L):
      return 0

   return sum(i[0] * i[1] for i in zip(K, L))


# # to be finished
# def equal_depth_bin_edges(dimension_, bin_count_):
#     return dimension_, bin_count_


# return bin_edge
def equal_width_bin_edges(dimension_, bin_count_):
    min_norm_ = 0
    max_norm_ = math.sqrt(dimension_)

    norm_range = float(max_norm_) - float(min_norm_)
    bin_range_ = norm_range / bin_count_

    bin_edges_ = []
    cur_norm = float(min_norm_)

    while float(cur_norm) <= float(max_norm_):
        bin_edges_.append(cur_norm)
        cur_norm = cur_norm + bin_range_

    print(bin_edges_.__len__())
    if bin_edges_.__len__() == bin_count_ and bin_edges_[bin_edges_.__len__() - 1] < max_norm_:
        bin_edges_.append(bin_edges_[bin_edges_.__len__() - 1] + bin_range_)
    elif bin_edges_[bin_edges_.__len__() - 1] <= max_norm_:
        bin_edges_[bin_edges_.__len__() - 1] = max(max_norm_ + 0.0000001, bin_edges_[bin_edges_.__len__() - 1] + 0.0000001)

    print(bin_edges_.__len__())
    print(bin_edges_)

    return np.asarray(bin_edges_)


def compute_bin_array(query_list_, query_num_, card_, data_list_, data_norm_list_, bins_, top_k_):
    save_bin_array = []
    total_counter = Counter()
    for ii in range(query_num_):
        print("Query index: " + str(ii))
        cur_query = query_list_[ii]
        inner_prod_list = []
        # temp_data_norm_list = data_norm_list
        # temp_data_norm_list = np.asarray(temp_data_norm_list)
        for jj in range(card_):
            cur_data = data_list_[jj]
            temp_dot_product = dot(cur_data, cur_query)
            inner_prod_list.append(temp_dot_product)
        inner_prod_list = np.asarray(inner_prod_list)
        reverse_sort_index = np.argsort((-inner_prod_list))
        top_k_index = reverse_sort_index[0: top_k_]

        selected_norms = data_norm_list_[list(top_k_index)]
        selected_inner_prod = inner_prod_list[list(top_k_index)]
        bin_count_array = np.digitize(selected_norms, bins_)
        save_bin_array.extend(bin_count_array)
        temp_counter = Counter(bin_count_array)
        total_counter = total_counter + temp_counter
    return np.asarray(save_bin_array), total_counter


def compute_cdf(sample_bins_range_, my_alpha_, my_beta_, min_index_, max_index_):
    sample_bin_max_ = max(sample_bins_range_)
    cur_index_ = min_index_ + 1
    weight_cdf_ = []

    while cur_index_ <= max_index_:
        if cur_index_ > sample_bin_max:
            temp_val1_ = beta.cdf(sample_bin_max_, my_alpha_, my_beta_, loc=min_index_, scale=max_index_ - min_index_)
            temp_val2_ = beta.cdf(cur_index_, my_alpha_, my_beta_, loc=min_index_, scale=max_index_ - min_index_)
            temp_val_ = temp_val2_ - temp_val1_
            weight_cdf_.append(temp_val_)
        else:
            temp_val_ = beta.cdf(cur_index_, my_alpha_, my_beta_, loc=min_index_, scale=max_index_ - min_index_)
            weight_cdf_.append(temp_val_)
        cur_index_ = cur_index_ + 1
    return np.asarray(weight_cdf_)


# partition the data based on the norm, save on file
def equal_width_partition_data(input_file_, dimension_, card_, bin_count_, data_type_, query_list_, query_num_, top_k_):
    data_norm_list, data_list = compute_norm(input_file_, dimension_, card_)
    max_norm = max(data_norm_list)
    min_norm = min(data_norm_list)

    # equal width
    bin_edge = equal_width_bin_edges(dimension_, bin_count_)

    print(min_norm)
    print(max_norm)
    print(bin_edge)

    digitize_index_ = np.digitize(data_list, bin_edge)

    # once having those bin_array, learn beta distribution through Counter() from each query
    bin_array_, total_counter_ = compute_bin_array(query_list_, query_num_, card_, data_list, data_norm_list, bin_edge, top_k_)
    min_index_ = 0
    max_index_ = bin_count_  # max bin number

    # learn beta distribution parameter
    my_alpha_, my_beta_ = compute_alpha_beta(bin_array_, min_index_, max_index_)
    sample_bins_range_ = list(total_counter_.keys())
    weight_cdf_list_ = compute_cdf(sample_bins_range_, my_alpha_, my_beta_, min_index_, max_index_)

    # following for hashing in the later phase
    data_type_ = data_type_ + 'equal_width_'
    save_bin_partition_on_file(bin_count_, data_type_, dimension_, card_, digitize_index_, data_list)

    return np.asarray(weight_cdf_list_)


# def equal_depth_partition_data(input_file_, dimension_, card_, bin_count_, data_type_, query_list_, query_num_, top_k_):
#     data_norm_list, data_list = compute_norm(input_file_, dimension_, card_)
#     max_norm = max(data_norm_list)
#     min_norm = min(data_norm_list)
#
#     # equal width
#     bin_edge = equal_depth_bin_edges(dimension_, bin_count_)
#
#     print(min_norm)
#     print(max_norm)
#     print(bin_edge)
#
#     digitize_index_ = np.digitize(data_list, bin_edge)
#
#     # once having those bin_array, learn beta distribution through Counter() from each query
#     bin_array_, total_counter_ = compute_bin_array(query_list_, query_num_, card_, data_list, data_norm_list, bin_edge,
#                                                    top_k_)
#     min_index_ = 0
#     max_index_ = bin_count_  # max bin number
#
#     # learn beta distribution parameter
#     my_alpha_, my_beta_ = compute_alpha_beta(bin_array_, min_index_, max_index_)
#     sample_bins_range_ = list(total_counter_.keys())
#     weight_cdf_list_ = compute_cdf(sample_bins_range_, my_alpha_, my_beta_, min_index_, max_index_)
#
#     # following for hashing in the later phase
#     data_type_ = data_type_ + 'equal_depth_'
#     save_bin_partition_on_file(bin_count_, data_type_, dimension_, card_, digitize_index_, data_list)
#
#     return np.asarray(weight_cdf_list_)


# to be tested
input_file_ = ''
dimension_ = 300
card_ = 17000
bin_count_ = 40
data_type_ = 'music' # load_query(query_folder_, dimension_)
query_list_ = []
query_num_ = 100
top_k_ = 25

cdf_list = equal_width_partition_data(input_file_, dimension_, card_, bin_count_, data_type_, query_list_, query_num_, top_k_)

print(cdf_list)
print(cdf_list.__len__())
print('Done')