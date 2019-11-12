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

#
# import random
# import numpy as np
# total_num = 50
# bin_count = 5
# bin_edges = []
# bin_edges.append(0)
# bin_edges.append(20)
# bin_edges.append(40)
# bin_edges.append(60)
# bin_edges.append(80)
# bin_edges.append(100)
#
#
# ii = 0
# list1 = []
# for ii in range(total_num):
#     number = random.randrange(1, 100, 1)
#     list1.append(number)
#
# card_per_bin = total_num / bin_count
# temp_index = np.argsort(list1)
#
# list2 = [list1[i] for i in temp_index]
#
# temp = np.array_split(list2, bin_count)
#
# bin_percentage = []
# for ii in range(bin_count):
#     temp_norm = temp[ii]
#     print(temp[ii], "min: ", min(temp[ii]), ", max: ", max(temp[ii]))
#     max_temp = max(temp[ii])
#     max_temp_index = -1
#     left_pivot = -1
#     right_pivot = -1
#     for jj in range(bin_edges.__len__()):
#         if max_temp < bin_edges[jj]:
#             max_temp_index = jj - 1
#             left_pivot = jj - 1
#             right_pivot = jj
#             break
#
#     temp_range = bin_edges[right_pivot] - bin_edges[left_pivot]
#     temp_add_on = max_temp - bin_edges[left_pivot]
#     temp_percentage = float(temp_add_on) / float(temp_range)
#     temp_bin_percentage = jj - 1 + temp_percentage
#     bin_percentage.append(temp_bin_percentage)
#
# print(bin_percentage)


from scipy.stats import beta

my_alpha_ = 364.48070953698357
my_beta_ = 183.7919664415109

min_index_ = 0
max_index_ = 40  # max bin number

temp_val_ = beta.ppf(0.05, my_alpha_, my_beta_, loc=min_index_, scale=max_index_ - min_index_)
print(temp_val_)


# return bin_edge
def equal_width_bin_edges(dimension_, bin_count_):
    min_norm_ = 0
    max_norm_ = math.sqrt(dimension_)

    norm_range = float(max_norm_) - float(min_norm_)
    bin_range_ = norm_range / bin_count_

    bin_edges_ = []
    cur_norm = float(min_norm_)

    while float(cur_norm) <= float(max_norm_):
        bin_edges_.append(cur_norm)
        cur_norm = cur_norm + bin_range_

    print("bin len before process: " + str(bin_edges_.__len__()))
    if bin_edges_.__len__() == bin_count_ and bin_edges_[bin_edges_.__len__() - 1] < max_norm_:
        bin_edges_.append(bin_edges_[bin_edges_.__len__() - 1] + bin_range_)
    elif bin_edges_[bin_edges_.__len__() - 1] <= max_norm_:
        bin_edges_[bin_edges_.__len__() - 1] = max(max_norm_ + 0.0000001, bin_edges_[bin_edges_.__len__() - 1] + 0.0000001)

    print("bin len after process: " + str(bin_edges_.__len__()))

    return bin_edges_


def compute_bin_percentage(data_norm_list_, bin_count_, bin_edges_equal_width_):
    partition_norm_list = np.array_split(data_norm_list_, bin_count_)
    bin_percentage = []
    for ii in range(bin_count_):
        temp_norm = partition_norm_list[ii]
        max_temp = max(partition_norm_list[ii])
        max_temp_index = -1
        left_pivot = -1
        right_pivot = -1
        for jj in range(bin_edges_equal_width_.__len__()):
            if max_temp < bin_edges_equal_width_[jj]:
                max_temp_index = jj - 1
                left_pivot = jj - 1
                right_pivot = jj
                break

        temp_range = bin_edges_equal_width_[right_pivot] - bin_edges_equal_width_[left_pivot]
        temp_add_on = max_temp - bin_edges_equal_width_[left_pivot]
        temp_percentage = float(temp_add_on) / float(temp_range)
        temp_bin_percentage = jj - 1 + temp_percentage
        bin_percentage.append(temp_bin_percentage)

    print(bin_percentage)
    return np.asarray(bin_percentage)


# given a float-bin index, compute the norm range
def compute_norm_range(bin_edges_equal_width_, bin_index_):
    low_end = math.floor(bin_index_)
    upper_end = math.ceil(bin_index_)
    low_norm = bin_edges_equal_width_[low_end]
    upper_norm = bin_edges_equal_width_[upper_end]
    target_norm = low_norm + (bin_index_ - low_end) * (upper_norm - low_norm)
    return target_norm


bin_edges_equal_width_ = [0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5, 2.75, 3.0, 3.25, 3.5, 3.75, 4.0,
                          4.25, 4.5, 4.75, 5.0, 5.25, 5.5, 5.75, 6.0, 6.25, 6.5, 6.75, 7.0, 7.25, 7.5, 7.75, 8.0, 8.25, 8.5, 8.75, 9.0, 9.25, 9.5, 9.75, 10.0000001]
# temp_val_ = temp_val_
target_norm = compute_norm_range(bin_edges_equal_width_, temp_val_)
print(target_norm)
test_array = np.asarray(list(range(40)))
print(test_array.__len__()) # 0 - 39
threshold = target_norm
# target = np.argwhere(test_array > 1 and test_array <= threshold)

target = np.where(np.logical_and(test_array > 1, test_array <= threshold))[0]
print(target)

print(target.__len__())

# print(target.flatten())
# target = target.flatten()
tt = test_array[target]

print(tt)
# for ii in range(target.__len__()):
#     index_num = target[ii][0]
#     print(index_num, test_array[index_num])









