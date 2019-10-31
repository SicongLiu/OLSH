import os
import re
import sys
import numpy as np
# import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# chunks = 25
# top_k = 25
# data_folder = '/Users/sicongliu/Desktop/Skyline_qhull_data/'
# data_type = ['anti_correlated_', 'correlated_', 'random_']
# dimension = 4
# cardinality = 200000

# for i in range(data_type.__len__()):
#     for j in range(25):
#         total_norm = 0
#         file_name = data_folder + data_type[i] + str(dimension) + '_' + str(cardinality) + '_qhull_layer_' + str(j)
#         # print("file name: " + file_name)
#         f = open(file_name, 'r')
#         lines = f.readlines()
#
#         cur_dim = int(lines[0])
#         cur_card = int(lines[1])
#         norm_list = []
#         for kk in range(cur_card):
#             current_data_record = np.fromstring(lines[kk + 2], dtype=float, sep=' ')
#             current_data_record = np.asarray(current_data_record)
#             temp_norm = np.linalg.norm(current_data_record)
#             norm_list.append(temp_norm)
#         f.close()
#
#         print('data type: ' + data_type[i] + ', cur_layer: ' + str(j + 1) + ', total # of data: ' + str(cur_card) + ', average norm: ' + str(np.mean(norm_list)) + ', min norm: '
#               + str(np.min(norm_list)) + ', max_norm: ' + str(np.max(norm_list)) + ', std: ' + str(np.std(norm_list)))


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
dimension = 60
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
min_norm = min(data_norm_list)
max_norm = max(data_norm_list)

# _ = plt.hist(data_norm_list, bins='auto')  # arguments are passed to np.histogram
# # plt.hist(data_norm_list, normed=True, bins=10)
#
# print("plot done")








# query_file_name = query_folder + 'query_' + str(dimension) + 'D.txt'
# f = open(query_file_name, 'r')
# lines = f.readlines()
# cur_dim = int(lines[0])
# cur_card = int(lines[1])
# query_list = []
# for kk in range(cur_card):
#     current_query_record = np.fromstring(lines[kk + 2], dtype=float, sep=' ')
#     current_query_record = np.asarray(current_query_record)
#     # temp_norm = np.linalg.norm(current_data_record)
#     query_list.append(current_query_record)
# f.close()
# query_list = np.asarray(query_list)

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
    save_current_qhull(save_base_folder, folder_name_index, temp_data_list, 'random', 100, cardinality, sorted_counter[i][1])



weight = []


print('Done')

# for ii in range(cardinality):
#     # cur_query = query_list[ii]
#     inner_prod_list = []
#     # temp_data_norm_list = data_norm_list
#     # temp_data_norm_list = np.asarray(temp_data_norm_list)
#     for jj in range(cardinality):
#         cur_data = data_list[jj]
#         # temp_dot_product = dot(cur_data, cur_query)
#         inner_prod_list.append(temp_dot_product)
#     inner_prod_list = np.asarray(inner_prod_list)
#     reverse_sort_index = np.argsort((-inner_prod_list))
#     top_k_index = reverse_sort_index[0: top_k]
#
#     selected_norms = data_norm_list[list(top_k_index)]
#     selected_inner_prod = inner_prod_list[list(top_k_index)]
#     bin_count_array = np.digitize(selected_norms, bins)
#     temp_counter = Counter(bin_count_array)
#     total_counter = total_counter + temp_counter

# cur_bins = np.histogram(data_norm_list, bins)
# bins_count = cur_bins[0]
# bins_range = cur_bins[1]
# print(bins_count)
# plt.hist(norm_list, normed=True, bins=30)
# plt.ylabel('Probability')

# # ==================== check top-25 how many elements in which bin ====================
# total_counter = Counter()
# for ii in range(query_num):
#     # cur_query = query_list[ii]
#     inner_prod_list = []
#     # temp_data_norm_list = data_norm_list
#     # temp_data_norm_list = np.asarray(temp_data_norm_list)
#     for jj in range(cardinality):
#         cur_data = data_list[jj]
#         # temp_dot_product = dot(cur_data, cur_query)
#         inner_prod_list.append(temp_dot_product)
#     inner_prod_list = np.asarray(inner_prod_list)
#     reverse_sort_index = np.argsort((-inner_prod_list))
#     top_k_index = reverse_sort_index[0: top_k]
#
#     selected_norms = data_norm_list[list(top_k_index)]
#     selected_inner_prod = inner_prod_list[list(top_k_index)]
#     bin_count_array = np.digitize(selected_norms, bins)
#     temp_counter = Counter(bin_count_array)
#     total_counter = total_counter + temp_counter
#
# # plt.bar(total_counter.keys(), total_counter.values())

