import os
import re
import sys
from openpyxl import load_workbook
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import math
from scipy.stats import beta


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
        print("Query index: " + str(ii))
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

    assert cur_dim == dim_
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


def calc_layer_ratio(qhull_folder_, data_type_, dim_, card_, topk, query_, query_count_, total_qhull_layer_, ground_truth_dot_):
    topk = min(topk, total_qhull_layer_)
    recall_ratio_ = []
    data_ratio_ = []
    for ii in range(topk):
        cur_qhull_file = qhull_folder_ + '_' + data_type_ + '_' + str(dim_) + '_' + str(card_) + '_qhull_layer_' + str(ii)
        cur_qhull_data_ = load_data(cur_qhull_file, dim_)

        layer_card_ratio = float(cur_qhull_data_.__len__())/float(card_)
        data_ratio_.append(layer_card_ratio)
        layer_recall_ratio = []
        for jj in range(query_count_):
            cur_query = query_[jj]
            temp_dot = calc_dot_rank(cur_query, cur_qhull_data_, topk)
            temp_ratio = calc_true_recall(temp_dot, ground_truth_dot_)
            layer_recall_ratio.append(temp_ratio)
        recall_ratio_.append(np.mean(layer_recall_ratio))
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
    layer_weight = []
    for ii in range(len(data_ratio_)):

        if ii == 0:
            cur_data_ratio = data_ratio_[ii]
            cur_weight = beta.cdf(cur_data_ratio, alpha_, beta_, loc=0, scale=1)
        else:
            cur_data_ratio = data_ratio_[ii]
            pre_data_ratio = data_ratio_[ii - 1]
            cur_weight = beta.cdf(cur_data_ratio, alpha_, beta_, loc=0, scale=1) - beta.cdf(pre_data_ratio, alpha_, beta_, loc=0, scale=1)
        layer_weight.append(cur_weight)
    return layer_weight


query_folder = '../H2_ALSH/qhull_data/Synthetic/'
raw_data_folder = '../H2_ALSH/raw_data/Synthetic/'
is_stats_learn = 1
dim = 2
card = 200000
topk = 25
min_val = 0
max_val = 1
data_type = ['anti_correlated', 'correlated', 'random']
query_list = load_query(query_folder, dim, is_stats_learn)
data_list = load_data(data_file, dim)
query_count = len(query_list)
ground_truth_dot = calc_ground_truth(query_list, query_count, data_list, topk)


recall_ratio, data_ratio = calc_layer_ratio(qhull_folder_, data_type_, dim_, card_, topk, query_, query_count_, total_qhull_layer_,
                     ground_truth_dot_)
alpha, beta = compute_alpha_beta(recall_ratio, min_val, max_val)
layer_wegith = calc_layer_weight(alpha, beta, data_ratio)


print('Done')



