import os
import re
import sys
import numpy as np
# import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import math


def split_original_query(query_folder_):
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

    return n_data_list, n_data_norm_list


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


data_folder = '../H2_ALSH/raw_data/Synthetic/'
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

# map(max, data_list)
# list(map(max, data_list))
# max_val = max(map(max, data_list))
#
# map(min, data_list)
# list(map(min, data_list))
# min_val = min(map(min, data_list))
#
# n_data_norm_list = []
# n_data_list = np.asarray((data_list - min_val)/(max_val - min_val))
# for kk in range(cur_card):
#     temp_norm = np.linalg.norm(n_data_list[kk])
#     n_data_norm_list.append(float("{0:.5f}".format(temp_norm)))

data_list, data_norm_list = scale_data(data_list)

chunks = 40
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

# plot without bin
_ = plt.hist(data_norm_list, bins='auto')  # arguments are passed to np.histogram

# plot with bin
_ = plt.hist(data_norm_list, bins=bin_array)  # arguments are passed to np.histogram
print("plot data norm done")

# plot maxium inner product of queries
query_list = load_query(query_folder, dimension, 0)
# ==================== check top-25 how many elements in which bin ====================
inner_prod_list = []
for ii in range(query_num):
    print("Query index: " + str(ii))
    cur_query = query_list[ii]
    inner_prod_list_temp = data_list.dot(cur_query)

    if inner_prod_list.__len__() ==0:
        inner_prod_list = list(inner_prod_list_temp)
    else:
        inner_prod_list.extend(list(inner_prod_list_temp))
    # for jj in range(cardinality):
    #     cur_data = data_list[jj]
    #     temp_dot_product = dot(cur_data, cur_query)
    #     inner_prod_list.append(temp_dot_product)
inner_prod_list = np.asarray(inner_prod_list)

# plot without bin
_ = plt.hist(inner_prod_list, bins='auto')  # arguments are passed to np.histogram

# plot with bin
_ = plt.hist(inner_prod_list, bins=bin_array)  # arguments are passed to np.histogram

print('Query top-k ground truth plot Done')

