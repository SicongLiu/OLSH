import os
import re
import sys
from openpyxl import load_workbook
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from scipy.io import loadmat
import os.path

def dot(K, L):
   if len(K) != len(L):
      return 0

   return sum(i[0] * i[1] for i in zip(K, L))


# merge RMT data
num_of_dimension = 128
RMT_data_size = 5
RMT_data_folder = "/Users/sliu104/Downloads/Features_RMT/"
total_feature = []
for ii in range(RMT_data_size):
    folder_index = ii + 1
    feature_file = RMT_data_folder + str(folder_index) + "/" + "feature_" + str(folder_index) + ".mat"
    if os.path.exists(feature_file):
        x = loadmat(feature_file)
        feature_frame = x['frame1']
        feature_frame = np.asarray(feature_frame)
        cur_feature = feature_frame[10:138, :]
        cur_feature = np.asarray(cur_feature, dtype=float)
        if total_feature.__len__() == 0:
            total_feature = list(cur_feature)
            total_feature = np.asarray(total_feature)
            total_feature = np.asmatrix(total_feature)
        else:
            total_feature = np.concatenate((total_feature, cur_feature), axis=1)



total_feature = np.asarray(total_feature, dtype=np.float)
total_feature = total_feature.transpose()
print(total_feature.__len__())
print(total_feature.shape)
total_count = total_feature.__len__()
save_folder = "/Users/sliu104/Desktop/StreamingTopK/H2_ALSH/raw_data/Synthetic/"
save_file = save_folder + "random_128_" + str(total_count)

total_data = []
total_data.append(np.asarray(int(num_of_dimension)))
total_data.append(np.asarray(int(total_count)))
total_data = np.asarray(total_data)
np.savetxt(save_file, total_data, delimiter=',', fmt='%i')

f_handle = open(save_file, 'ab')
# np.savetxt(f_handle, total_feature, fmt='%10.6f')
np.savetxt(f_handle, total_feature)
f_handle.close()

print("merging features done")







# chunks = 20
# top_k = 25
# query_num = 100
# data_folder = '/Users/sicongliu/Desktop/StreamingTopK/H2_ALSH/raw_data/Synthetic/'
# query_folder = '/Users/sicongliu/Desktop/StreamingTopK/H2_ALSH/query/'
# # data_type = ['anti_correlated_', 'correlated_', 'random_']
# data_type = 'random_'
# dimension = 80
# cardinality = 100000
#
# file_name = data_folder + data_type + str(dimension) + '_' + str(cardinality) + '.txt'
# f = open(file_name, 'r')
# lines = f.readlines()
#
# cur_dim = int(lines[0])
# cur_card = int(lines[1])
# data_norm_list = []
# data_list = []
# for kk in range(cur_card):
#     current_data_record = np.fromstring(lines[kk + 2], dtype=float, sep=' ')
#     current_data_record = np.asarray(current_data_record)
#     data_list.append(current_data_record)
#     # temp_norm = float(format(np.linalg.norm(current_data_record), '.7f'))
#     temp_norm = np.linalg.norm(current_data_record)
#     data_norm_list.append(temp_norm)
# f.close()
# data_norm_list = np.asarray(data_norm_list)
#
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
#
# # ==================== load data into bin ====================
# min_norm = min(data_norm_list)
# max_norm = max(data_norm_list)
# norm_range = float(max_norm) - float(min_norm)
# bin_size = norm_range / chunks
#
# bin_array = []
# cur_norm = float(min_norm)
#
# while float(cur_norm) <= float(max_norm):
#     bin_array.append(cur_norm)
#     cur_norm = cur_norm + bin_size
#
# # bin_array[0] = min(min_norm - 0.000001, bin_array[0] - 0.000001)
# print(bin_array.__len__())
# if bin_array.__len__()  == chunks and bin_array[bin_array.__len__() - 1] < max_norm:
#     bin_array.append(bin_array[bin_array.__len__() - 1] + bin_size)
# elif bin_array[bin_array.__len__() - 1] <= max_norm:
#     bin_array[bin_array.__len__() - 1] = max(max_norm + 0.0000001, bin_array[bin_array.__len__() - 1] + 0.0000001)
# # bin_array[bin_array.__len__() - 1] = max(max_norm + 0.0000001, bin_array[bin_array.__len__() - 1] + 0.0000001)
#
# print(bin_array.__len__())
# print(bin_array)
#
# bins = np.array(bin_array)
# # cur_bins = np.histogram(data_norm_list, bins)
# # bins_count = cur_bins[0]
# # bins_range = cur_bins[1]
# # print(bins_count)
# # plt.hist(norm_list, normed=True, bins=30)
# # plt.ylabel('Probability')
#
# # ==================== check top-25 how many elements in which bin ====================
# total_counter = Counter()
# for ii in range(query_num):
#     print("Query index: " + str(ii))
#     cur_query = query_list[ii]
#     inner_prod_list = []
#     # temp_data_norm_list = data_norm_list
#     # temp_data_norm_list = np.asarray(temp_data_norm_list)
#     for jj in range(cardinality):
#         cur_data = data_list[jj]
#         temp_dot_product = dot(cur_data, cur_query)
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
# plt.bar(total_counter.keys(), total_counter.values())
#
# print('Done')