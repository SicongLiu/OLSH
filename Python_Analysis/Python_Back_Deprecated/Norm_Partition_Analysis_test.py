import os
import re
import sys
import numpy as np
# import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import math


def sigmoid(x):
  return 1 / (1 + math.exp(-x))


def compute_weight(sorted_counter, cardinality_):
    weight = []
    bin_factor_list = []
    data_size_factor_list = []
    total_bin_count_ = sorted_counter.__len__()
    for i in reversed(range(sorted_counter.__len__())):
        bin_index = i + 1
        layer_index = top_k - (i + 1)
        temp_bin_factor_ = float(bin_index) / float(total_bin_count_)
        bin_factor_ = sigmoid(temp_bin_factor_)
        bin_factor_list.append(bin_factor_)
        data_size_factor_ = sigmoid(float(sorted_counter[i][1])/float(cardinality_))
        data_size_factor_list.append(data_size_factor_)
        temp_weight = bin_factor_ * data_size_factor_
        weight.append(temp_weight)
    print(bin_factor_list)
    print(data_size_factor_list)
    return weight


def save_current_qhull(folder_name_, layer_index_, data_, data_type_, dimension_, cardinality_, data_size_):
    file_name = folder_name_ + data_type_ + '_' + str(dimension_) + '_' + str(cardinality_) + '_qhull_layer_' + str(layer_index_)
    save_data = []
    save_data.append(np.asarray(int(dimension_)))
    save_data.append(np.asarray(int(data_size_)))
    save_data = np.asarray(save_data)
    np.savetxt(file_name, save_data, delimiter=',', fmt='%i')

    f_handle = open(file_name, 'ab')
    np.savetxt(f_handle, data_, fmt='%10.6f')
    f_handle.close()

def dot(K, L):
   if len(K) != len(L):
      return 0

   return sum(i[0] * i[1] for i in zip(K, L))


chunks = 25
top_k = 25
query_num = 100
# data_folder = '/Users/sliu104/Desktop/StreamingTopK/H2_ALSH/qhull_data/Synthetic/'
data_folder = '/Users/sliu104/Desktop/StreamingTopK/H2_ALSH/raw_data/Synthetic/'
query_folder = '~/Desktop/StreamingTopK/H2_ALSH/query/'
# data_type = ['anti_correlated_', 'correlated_', 'random_']
data_type = 'random_'
dimension = 100
cardinality = 100000
layer_index = 0
bins = 25


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
# _ = plt.hist(data_norm_list, bins='auto')  # arguments are passed to np.histogram
# # plt.hist(data_norm_list, normed=True, bins=10)
#
# print("plot done")


# ==================== load data into bin ====================
min_norm = min(data_norm_list)
max_norm = max(data_norm_list)

norm_range = max_norm - min_norm
bin_size = norm_range / chunks

bin_array = []
cur_norm = min_norm

float("{0:.2f}".format(max_norm))

while float("{0:.5f}".format(cur_norm)) <= float("{0:.5f}".format(max_norm)):
    bin_array.append(cur_norm)
    cur_norm = cur_norm + bin_size

print(bin_array)
print(bin_array.__len__())
bins = np.array(bin_array)

bin_count_array = np.digitize(data_norm_list, bins)

total_counter = Counter(bin_count_array)
sorted_counter = sorted(total_counter.items())
# plt.bar(total_counter.keys(), total_counter.values())
print(total_counter)
print(sum(total_counter.values()))
print(sorted_counter)
print(sorted_counter.__len__())

for ii in range(sorted_counter.__len__()):
    print(str(sorted_counter[ii][0]) + ' ' + str(sorted_counter[ii][1]) )

# save those partitions to file
save_base_folder = './'
for i in reversed(range(sorted_counter.__len__())):
    bin_index = i + 1
    # find data index and data
    item_index = np.where(bin_count_array == bin_index)
    temp_data_list = data_list[item_index[0]]
    temp_data_list = np.asarray(temp_data_list)
    folder_name_index = top_k - (i + 1)
    save_folder = save_base_folder + 'random_100_100000_qhull_layer_' + str(folder_name_index)
    print(temp_data_list.__len__())
    # save_current_qhull(save_base_folder, folder_name_index, temp_data_list, 'random', 100, cardinality, sorted_counter[i][1])

weight = compute_weight(sorted_counter, cardinality)
print(weight)

print('Done')
