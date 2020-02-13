import os
import re
import sys
from openpyxl import load_workbook
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import math
from scipy.stats import beta
import scipy.stats as stats


# def plot_beta(alpha_, beta_):


def load_query(query_folder_, dimension_, is_stats_learn_):
    if is_stats_learn_:
        query_file_name = query_folder_ + 'query_' + str(dimension_) + 'D_stats_learn.txt'
    else:
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


def calc_ground_truth(query_data_, query_count_, data_, topk):
    ground_truth_dot = []
    for ii in range(query_count_):
        # print("Query index: " + str(ii))
        cur_query = query_data_[ii]
        cur_query = np.asarray(cur_query)
        cur_ground_truth_dot = calc_dot_rank(cur_query, data_, topk)
        ground_truth_dot.append(cur_ground_truth_dot)
    return ground_truth_dot


def calc_dot_rank(query_data_, data_, topk):
    query_data_ = np.asarray(query_data_)
    inner_prod_list = data_.dot(query_data_)
    inner_prod_list = np.asarray(inner_prod_list)
    reverse_sort_index = np.argsort((-inner_prod_list))
    top_k_index = reverse_sort_index[0: topk]
    selected_dot_values_ = inner_prod_list[list(top_k_index)]
    return selected_dot_values_


def load_data(data_file_, dim_):
    f = open(data_file_, 'r')
    lines = f.readlines()
    cur_dim = int(lines[0])
    cur_card = int(lines[1])

    assert int(cur_dim) + 1 == int(dim_)
    data_list = []
    for kk in range(cur_card):
        current_data_record = np.fromstring(lines[kk + 2], dtype=float, sep=' ')
        current_data_record = np.asarray(current_data_record)
        data_list.append(current_data_record)
    f.close()
    data_list = np.asarray(data_list)
    return data_list


def calc_true_recall(val_list_, ground_truth_, topk):
    temp_index_ = topk - 1
    last_index_ = topk - 1
    while temp_index_ >= 0 and ground_truth_[last_index_] - val_list_[temp_index_] > 0:
        temp_index_ = temp_index_ - 1
    return float(temp_index_ + 1)/float(topk)


def calc_layer_ratio(qhull_folder_, data_type_, dim_, card_, total_layer_, topk, query_, query_count_, total_qhull_layer_, ground_truth_dot_):
    topk = min(topk, total_qhull_layer_)
    recall_ratio_ = []
    indexed_data_ = []
    for ii in range(topk):
        cur_qhull_file = qhull_folder_ + data_type_ + '_' + str(dim_) + '_' + str(card_) + '_qhull_layer_' + str(ii)
        cur_qhull_data_ = load_data(cur_qhull_file, dim_)
        indexed_data_.append(cur_qhull_data_.__len__())
        # layer_card_ratio = float(cur_qhull_data_.__len__())/float(card_)
        layer_recall_ratio = []
        for jj in range(query_count_):
            cur_query = query_[jj]
            temp_dot = calc_dot_rank(cur_query, cur_qhull_data_, topk)
            # need to be adapted to the layer elements
            while len(temp_dot) < topk:
                temp_dot = np.append(temp_dot, -1.0)
            temp_ratio = calc_true_recall(temp_dot, ground_truth_dot_[jj], topk)
            layer_recall_ratio.append(temp_ratio)
        recall_ratio_.append(np.mean(layer_recall_ratio))
    indexed_data_ = np.asarray(indexed_data_)
    total_indexed_data_ = np.sum(indexed_data_)
    # data_ratio_ = float(indexed_data_)/float(total_indexed_data_)
    data_ratio_ = np.divide(indexed_data_, total_indexed_data_)
    return recall_ratio_, data_ratio_


def compute_alpha_beta(input_ndarray_, min_val_, max_val_):
    sample_mean = np.mean(input_ndarray_)
    sample_var = np.var(input_ndarray_, ddof=1)
    x_bar = float(sample_mean - min_val_) / float(max_val_ - min_val_)
    var_bar = float(sample_var) / math.pow(float(max_val_ - min_val_), 2)
    alpha_ = x_bar * (x_bar * (1 - x_bar)/var_bar - 1)
    beta_ = (1 - x_bar) * (x_bar * (1 - x_bar)/var_bar - 1)

    return alpha_, beta_


def calc_layer_weight(alpha_, beta_, data_ratio_):
    beta_weight = []
    for ii in range(data_ratio_.__len__()):
        if ii == 0:
            cur_weight = beta.cdf(ii, alpha_, beta_, loc=1, scale=data_ratio_.__len__())
        else:
            t1 = beta.cdf(ii, alpha_, beta_, loc=1, scale=data_ratio_.__len__())
            t2 = beta.cdf(ii + 1, alpha_, beta_, loc=1, scale=data_ratio_.__len__())
            cur_weight = t2 - t1
            beta_weight.append(cur_weight)
    beta_weight.append(0)
    return beta_weight


qhull_folder = '../H2_ALSH/qhull_data/Synthetic/'
# qhull_folder = './'
raw_data_folder = '../H2_ALSH/raw_data/Synthetic/'
is_stats_learn = 1
# dims = [2, 3, 4, 5]
# dims = [4]
dims = [2, 3, 4, 5, 6, 7]
cards = [200000]
# cards = [500000, 1000000, 1500000, 2000000]
# cards = [500000]
topk = 25

data_types = ['anti_correlated', 'correlated', 'random']

# data_types = ['anti_correlated']
total_qhull_layer = topk
for dim in dims:
    for card in cards:
        for data_type in data_types:
            if dim == 5 and card == 200000:
                if data_type == 'anti_correlated':
                    total_qhull_layer = 10
                elif data_type == 'correlated':
                    total_qhull_layer = 25
                else:
                    total_qhull_layer = 25
            elif dim == 4 and card == 500000:
                if data_type == 'anti_correlated':
                    total_qhull_layer = 21
                elif data_type == 'correlated':
                    total_qhull_layer = 25
                else:
                    total_qhull_layer = 25
            elif dim == 6 and card == 200000:
                if data_type == 'anti_correlated':
                    total_qhull_layer = 7
                elif data_type == 'correlated':
                    total_qhull_layer = 25
                else:
                    total_qhull_layer = 17
            elif dim == 7 and card == 200000:
                if data_type == 'anti_correlated':
                    total_qhull_layer = 5
                elif data_type == 'correlated':
                    total_qhull_layer = 25
                else:
                    total_qhull_layer = 13

            for ii in range(total_qhull_layer):
                cur_qhull_file = qhull_folder + data_type + '_' + str(dim) + '_' + str(
                    card) + '_qhull_layer_' + str(ii)
                cur_qhull_data_ = load_data(cur_qhull_file, dim + 1)
                updated_qhull_data = np.delete(cur_qhull_data_, np.s_[-1:], axis=1)
                # save it back to the same file
                num_of_dimension = dim
                num_of_points = updated_qhull_data.__len__()
                data_info = []

                data_info.append(np.asarray(int(num_of_dimension)))
                data_info.append(np.asarray(int(num_of_points)))
                data_info = np.asarray(data_info)
                np.savetxt(cur_qhull_file, data_info, delimiter=',', fmt='%i')

                # separate metadata and data points, appending data points to metadata text saved on file
                f_handle = open(cur_qhull_file, 'ab')
                np.savetxt(f_handle, updated_qhull_data, fmt='%.6f')
                f_handle.close()
print('Done')



