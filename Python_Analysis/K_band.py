import os
import re
import sys
import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
from collections import Counter

def dot(K, L):
   if len(K) != len(L):
      return 0

   return sum(i[0] * i[1] for i in zip(K, L))


chunks = 25
top_k = 25
query_num = 100
data_folder = '/Users/sliu104/Desktop/StreamingTopK/H2_ALSH/qhull_data/Synthetic/'
raw_data_folder = '/Users/sliu104/Desktop/StreamingTopK/H2_ALSH/raw_data/Synthetic/'
query_folder = '~/Desktop/StreamingTopK/H2_ALSH/query/'
# data_type = ['anti_correlated_', 'correlated_', 'random_']
data_type = 'random_'
dimension = 100
cardinality = 100000
layer_index = 0
bins = 25


# file_name = data_folder + data_type + str(dimension) + '_' + str(cardinality) + '_qhull_layer_' + str(layer_index)
file_name = raw_data_folder + data_type + str(dimension) + '_' + str(cardinality)
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

# save index from bin_count_array into
data_list = np.asarray(data_list)
bin_count_array = np.asarray(bin_count_array)
for ii in range(top_k):
    file_name = data_folder + data_type + str(dimension) + '_' + str(cardinality) + '_qhull_layer_' + str(ii)
    search_key = top_k - ii
    temp_index = np.where(bin_count_array == search_key)[0]
    print(temp_index)
    temp_cardinality = temp_index.size

    data_to_be_save = []
    data_to_be_save.append(np.asarray(int(dimension)))
    data_to_be_save.append(np.asarray(int(temp_cardinality)))
    data_to_be_save = np.asarray(data_to_be_save)

    np.savetxt(file_name, data_to_be_save, delimiter=',', fmt='%i')

    current_qhull_list_output = data_list[temp_index, :]
    # separate metadata and data points, appending data points to metadata text saved on file
    f_handle = open(file_name, 'ab')
    np.savetxt(f_handle, current_qhull_list_output, fmt='%10.6f')
    f_handle.close()
    print("layer - " + str(ii) + " done")

print('Done')
