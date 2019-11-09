import numpy as np
# x = np.array([3, 4])
# y = np.linalg.norm(x)
#
# yy = np.std(x)

# import matplotlib.pyplot as plt
import math
from  collections import Counter
import random

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

# print(1.0 * sum(dim_1)/dim_1.__len__())
# print(1.0 * sum(dim_10)/dim_10.__len__())
# print(1.0 * sum(dim_15)/dim_15.__len__())
# print(1.0 * sum(dim_20)/dim_20.__len__())
# print(1.0 * sum(dim_25)/dim_25.__len__())
# print(1.0 * sum(dim_50)/dim_50.__len__())
# print(1.0 * sum(dim_75)/dim_75.__len__())


def gen_hash_tables(top_k_):
    hashTables = []
    start_char = 'a'
    temp_prefix = ''
    for ii in range(top_k_):
        temp_index = ii
        start_char_length = float(temp_index) / 26
        start_char_diff = temp_index % 26
        temp_char = chr(ord(start_char) + start_char_diff)

        if math.floor(start_char_length) > temp_prefix.__len__():
            temp_prefix = temp_prefix + 'a'
        temp_char = temp_prefix + temp_char
        hashTables.append(temp_char)

    result_ = ', '.join(hashTables)
    return result_


import random
import numpy as np
total_num = 50
bin_count = 5
bin_edges = []
bin_edges.append(0)
bin_edges.append(20)
bin_edges.append(40)
bin_edges.append(60)
bin_edges.append(80)
bin_edges.append(100)


ii = 0
list1 = []
for ii in range(total_num):
    number = random.randrange(1, 100, 1)
    list1.append(number)

card_per_bin = total_num / bin_count
temp_index = np.argsort(list1)

list2 = [list1[i] for i in temp_index]

temp = np.array_split(list2, bin_count)

bin_percentage = []
for ii in range(bin_count):
    temp_norm = temp[ii]
    print(temp[ii], "min: ", min(temp[ii]), ", max: ", max(temp[ii]))
    max_temp = max(temp[ii])
    max_temp_index = -1
    left_pivot = -1
    right_pivot = -1
    for jj in range(bin_edges.__len__()):
        if max_temp < bin_edges[jj]:
            max_temp_index = jj - 1
            left_pivot = jj - 1
            right_pivot = jj
            break

    temp_range = bin_edges[right_pivot] - bin_edges[left_pivot]
    temp_add_on = max_temp - bin_edges[left_pivot]
    temp_percentage = float(temp_add_on) / float(temp_range)
    temp_bin_percentage = jj - 1 + temp_percentage
    bin_percentage.append(temp_bin_percentage)

print(bin_percentage)
