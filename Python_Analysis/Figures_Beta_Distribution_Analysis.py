import os
import re
import sys
import numpy as np
# import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import math
from scipy.stats import beta
from matplotlib.patches import Rectangle


def compute_alpha_beta(input_ndarray_, min_index_, max_index_):
    sample_mean = np.mean(input_ndarray_)
    sample_var = np.var(input_ndarray_, ddof=1)
    x_bar = float(sample_mean - min_index_) / float(max_index_ - min_index_)
    var_bar = float(sample_var) / math.pow(float(max_index_ - min_index_), 2)
    alpha_ = x_bar * (x_bar * (1 - x_bar)/var_bar - 1)
    beta_ = (1 - x_bar) * (x_bar * (1 - x_bar)/var_bar - 1)

    return alpha_, beta_


def compute_bin_array(query_list_, query_num_, data_list_, data_norm_list_, bins_, top_k_):
    ret_norm_list = []
    save_bin_array = []
    total_counter = Counter()
    data_list_ = np.asarray(data_list_)
    for ii in range(query_num_):
        print("Query index: " + str(ii))
        cur_query = query_list_[ii]
        cur_query = np.asarray(cur_query)
        inner_prod_list = data_list_.dot(cur_query)

        inner_prod_list = np.asarray(inner_prod_list)
        reverse_sort_index = np.argsort((-inner_prod_list))
        top_k_index = reverse_sort_index[0: top_k_]

        selected_norms = data_norm_list_[list(top_k_index)]
        selected_inner_prod = inner_prod_list[list(top_k_index)]
        ret_norm_list.extend(selected_inner_prod)
        bin_count_array = np.digitize(selected_norms, bins_)
        save_bin_array.extend(bin_count_array)
        temp_counter = Counter(bin_count_array)
        total_counter = total_counter + temp_counter
    return np.asarray(save_bin_array), total_counter, np.asarray(ret_norm_list)


def split_original_query(query_folder_, dimension_):
    query_file_name = query_folder_ + 'query_' + str(dimension_) + 'D_original.txt'
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

    updated_card = cur_card / 2
    stats_learn_query_file = 'query_' + str(cur_dim) + 'D_stats_learn.txt'
    stats_learn_query = query_list[0: updated_card]
    temp_batch = []
    temp_batch.append(np.asarray(int(cur_dim)))
    temp_batch.append(np.asarray(int(updated_card)))
    temp_batch = np.asarray(temp_batch)
    np.savetxt(stats_learn_query_file, temp_batch, delimiter=',', fmt='%i')

    temp_data_bash = np.asarray(stats_learn_query)
    f_handle = open(stats_learn_query_file, 'ab')
    np.savetxt(f_handle, temp_data_bash, fmt='%10.6f')
    f_handle.close()

    test_query_file = 'query_' + str(cur_dim) + 'D.txt'
    test_query = query_list[updated_card: cur_card]
    temp_batch = []
    temp_batch.append(np.asarray(int(cur_dim)))
    temp_batch.append(np.asarray(int(updated_card)))
    temp_batch = np.asarray(temp_batch)
    np.savetxt(test_query_file, temp_batch, delimiter=',', fmt='%i')

    temp_data_bash = np.asarray(test_query)
    f_handle = open(test_query_file, 'ab')
    np.savetxt(f_handle, temp_data_bash, fmt='%10.6f')
    f_handle.close()

    return np.asarray(query_list)


def scale_data(data_list_):
    map(max, data_list_)
    list(map(max, data_list_))
    max_val = max(map(max, data_list_))

    map(min, data_list_)
    list(map(min, data_list_))
    min_val = min(map(min, data_list_))

    n_data_norm_list = []
    n_data_list = np.asarray((data_list_ - min_val) / (max_val - min_val))
    for kk in range(cur_card):
        temp_norm = np.linalg.norm(n_data_list[kk])
        n_data_norm_list.append(float("{0:.5f}".format(temp_norm)))

    return np.asarray(n_data_list), np.asarray(n_data_norm_list)


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

def dot(K, L):
   if len(K) != len(L):
      return 0

   return sum(i[0] * i[1] for i in zip(K, L))


# Real_life data:
# 300D: Netflix
# 192D: YahooMusic

data_folder = '../H2_ALSH/raw_data/Synthetic/bak/'
# data_type = ['anti_correlated_', 'correlated_', 'random_']
data_type = 'random_'
dimension = 192
cardinality = 53387

query_num = 1000
query_folder = '../H2_ALSH/query/'
query_file = query_folder + 'query_' + str(dimension) + 'D.txt'

file_name = data_folder + data_type + str(dimension) + '_' + str(cardinality) + '.txt'
f = open(file_name, 'r')
lines = f.readlines()

cur_dim = int(lines[0])
cur_card = int(lines[1])
data_norm_list = []
data_list = []
for kk in range(cur_card):
    current_data_record = np.fromstring(lines[kk + 2], dtype=float, sep=' ')
    current_data_record = np.asarray(current_data_record)
    data_list.append(current_data_record)
    temp_norm = np.linalg.norm(current_data_record)
    # data_norm_list.append(format(temp_norm, '.5f'))
    data_norm_list.append(float("{0:.5f}".format(temp_norm)))

f.close()
data_norm_list = np.asarray(data_norm_list)
data_list = np.asarray(data_list)

data_list, data_norm_list = scale_data(data_list)

# save_date_folder = '../H2_ALSH/raw_data/Synthetic/'
# save_file_name = save_date_folder + data_type + str(dimension) + '_' + str(cardinality) + '.txt'
#
#
# num_of_dimension = dimension
# num_of_points = cardinality
# data_info = []
# data_info.append(np.asarray(int(num_of_dimension)))
# data_info.append(np.asarray(int(num_of_points)))
# data_info = np.asarray(data_info)
# np.savetxt(save_file_name, data_info, delimiter=',', fmt='%i')
#
# # separate metadata and data points, appending data points to metadata text saved on file
# f_handle = open(save_file_name, 'ab')
# np.savetxt(f_handle, data_list, fmt='%.6f')
# f_handle.close()

print('Done')



chunks = 40
top_k = 25
# min_norm = 0
# max_norm = math.sqrt(dimension)
min_norm = min(data_norm_list)
max_norm = max(data_norm_list)

norm_range = float(max_norm) - float(min_norm)
bin_size = norm_range / chunks

bin_array = []
cur_norm = float(min_norm)

while float(cur_norm) <= float(max_norm):
    bin_array.append(cur_norm)
    cur_norm = cur_norm + bin_size

# bin_array[0] = min(min_norm - 0.000001, bin_array[0] - 0.000001)
print(bin_array.__len__())
if bin_array.__len__() == chunks and bin_array[bin_array.__len__() - 1] < max_norm:
    bin_array.append(bin_array[bin_array.__len__() - 1] + bin_size)
elif bin_array[bin_array.__len__() - 1] <= max_norm:
    bin_array[bin_array.__len__() - 1] = max(max_norm + 0.0000001, bin_array[bin_array.__len__() - 1] + 0.0000001)

# bin_array[bin_array.__len__() - 1] = max(max_norm + 0.0000001, bin_array[bin_array.__len__() - 1] + 0.0000001)
print(bin_array.__len__())

# _ = plt.hist(data_norm_list, bins='auto')  # arguments are passed to np.histogram
# plt.xlabel("norm values", fontsize=14)
# plt.ylabel("frequency", fontsize=14)
# plt.xticks(fontsize=14)
# plt.yticks(fontsize=14)

#create legend
# handles = [Rectangle((0, 0), 1, 1, ec="k")]
# labels = ["test"]
# plt.legend(handles, labels)
print("plot data norm done")

# plot maxium inner product of queries
query_list = load_query(query_folder, dimension, 0)
bin_array, total_counter, top_k_prod = compute_bin_array(query_list, query_num, data_list, data_norm_list, bin_array, top_k)


# _ = plt.hist(top_k_prod, bins='auto')  # arguments are passed to np.histogram
# plt.xlabel("top-k inner product", fontsize=14)
# plt.ylabel("frequency", fontsize=14)
# plt.xticks(fontsize=14)
# plt.yticks(fontsize=14)

# plt.bar(total_counter.keys(), total_counter.values())
# plt.xlabel("top-k inner product partition index", fontsize=14)
# plt.ylabel("frequency", fontsize=14)


min_index = 0
max_index = chunks
my_alpha_, my_beta_ = compute_alpha_beta(bin_array, min_index, max_index)

x = np.arange(0.01, max_index, 0.01)
y = beta.pdf(x, my_alpha_, my_beta_, loc=min_index, scale=max_index - min_index)

plt.plot(x, y)
# plt.xlabel("distribution of partition index and frequency", fontsize=14)
# plt.ylabel("probability", fontsize=14)
print('Query top-k ground truth plot Done')

