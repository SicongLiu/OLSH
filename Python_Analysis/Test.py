import numpy as np
# x = np.array([3, 4])
# y = np.linalg.norm(x)
#
# yy = np.std(x)

import matplotlib.pyplot as plt
import math
from  collections import Counter
import random
from scipy.stats import beta

recall_list = []
dim_1 = []
dim_1.append(0.01)
dim_1.append(0.0072)
dim_1.append(0.0189333333333)

dim_10 = []
dim_10.append(0.2636)
dim_10.append(0.2696)
dim_10.append(0.2756)

dim_15 = []
dim_15.append(0.3708)
dim_15.append(0.3456)
dim_15.append(0.402533333333)

dim_20 = []
dim_20.append(0.3628)
dim_20.append(0.4106)
dim_20.append(0.394666666667)

dim_25 = []
dim_25.append(0.6156)
dim_25.append(0.5184)
dim_25.append(0.507066666667)

dim_50 = []
dim_50.append(0.7224)
dim_50.append(0.764)
dim_50.append(0.762133333333)

dim_75 = []
dim_75.append(0.9144)
dim_75.append(0.8788)
dim_75.append(0.880133333333)

# test_file = './query_test.txt'
# f = open(test_file, 'r')
# lines = f.readlines()
# cur_dim = int(lines[0])
# cur_card = int(lines[1])
# query_list = []
# for kk in range(cur_card):
#     current_query_record = np.fromstring(lines[kk + 2], dtype=float, sep=' ')
#     current_query_record = np.asarray(current_query_record)
#     query_list.append(current_query_record)
# f.close()
import re
def separate_string(input_string):
    items = []
    match = re.match(r"([a-z]+)([0-9]+)", input_string, re.I)
    if match:
        items = match.groups()
    return items

def colnum_string(n):
    string = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        string = chr(65 + remainder) + string
    return string

import string
def col2num(col):
    num = 0
    for c in col:
        if c in string.ascii_letters:
            num = num * 26 + (ord(c.upper()) - ord('A')) + 1
    return num



data_list_ = ['J6',  'J45', 'J51', 'J90']
k_ranges = ['E6',  'E45', 'E51', 'E90']
l_ranges_opt = ['F6', 'F45']
l_ranges_max = ['G6', 'G45']
l_ranges_uni = ['H6', 'H45']


# J, AA AQ
# Data_Types = ['anti_correlated', 'correlated', 'random']
def compute_data_list_start_end(data_type_index_, data_list, column_dist_):
    start_items_ = separate_string(data_list[0])
    start_letter_ = start_items_[0]
    start_num_ = start_items_[1]

    end_items_ = separate_string(data_list[1])
    end_letter_ = end_items_[0]
    end_num_ = end_items_[1]

    start_letter_integer_ = int(col2num(start_letter_))
    start_letter_integer_ = start_letter_integer_ + column_dist_ * data_type_index_
    start_letter_ = colnum_string(start_letter_integer_)
    data_list_start = start_letter_ + start_num_
    data_list_end = start_letter_ + end_num_

    return data_list_start, data_list_end


# both letter and integer row index change
def compute_ranges_start_end(column_shift, row_shift, ranges, row_dist_, column_dist_):
    range_start, range_end = compute_data_list_start_end(column_shift, ranges, column_dist_)
    range_column = separate_string(range_start)[0]
    range_row_start = separate_string(range_start)[1] # 6
    range_row_end = separate_string(range_end)[1] # 45
    row_span_ = int(range_row_end) - int(range_row_start)

    target_row_start = int(range_row_end) * row_shift + row_dist_ # 51
    target_row_end = target_row_start + row_span_
    k_ranges_temp_start = range_column + str(target_row_start)
    k_ranges_temp_end = range_column + str(target_row_end)

    return k_ranges_temp_start, k_ranges_temp_end


def compute_hash_cell(l_ranges_opt_temp_end, temp_row_dist, temp_column_dist):
    temp_column = separate_string(l_ranges_opt_temp_end)[0]
    temp_row = int(separate_string(l_ranges_opt_temp_end)[1])
    final_column = colnum_string(col2num(temp_column) + temp_column_dist)
    final_row = temp_row + temp_row_dist
    hash_used_cell = final_column + str(final_row)
    return hash_used_cell


import math



def millify(n):
    millnames = ['', 'K', 'M']
    n = float(n)
    millidx = max(0, min(len(millnames)-1, int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))

    return '{:.00f}{}'.format(n / 10**(3 * millidx), millnames[millidx])


# list1 = [1, 4, 34, 34, 6, 8, 7, 32, 54, 346, 6, 10]
# list1 = np.asarray(list1)
# print(list1)
#
# length = len(list1)
# cut_length = int(length * 0.5)
# list2 = list1[0:cut_length]
# print(list2)
#
# list3 = list1[cut_length: length]
# print(length, cut_length)
#
# print(list3)
#
# test_matrix_ = np.random.rand(5, 5)
# test_matrix_ = np.asarray(test_matrix_)
# print(test_matrix_)
#
# numrows = len(test_matrix_)
# numcols = len(test_matrix_[0])
#
# print(test_matrix_[:, 1])
# print(test_matrix_[1, :])



# data_list = np.random.rand(2,3)
#
# print(data_list)
#
# map(min, data_list)
# list(map(min, data_list))
# min_val = min(map(min, data_list))
#
# map(max, data_list)
# list(map(max, data_list))
# max_val = max(map(max, data_list))
#
# inter_val = max_val - min_val
#
# tt = (data_list - min_val)/max_val

a = 5
b = 2.8

x = np.arange(0.01, 1, 0.01)
y = beta.pdf(x, a, b)
# plt.plot(x,y)

plt.plot(x, y)
plt.xticks([])
plt.yticks([])
# plt.plot(x, y1, "-", x, y2, "r--", x, y3, "g--")
print('all done')









