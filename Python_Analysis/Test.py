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


# top_k = 52
# rr = gen_hash_tables(top_k)
# text = "this is it: " + rr
# print(text)

tt = 7.73524942e-83
print(tt)
ttt = '{:.20f}'.format(tt)
list1 = []
list1.append(ttt)
list1.append(ttt)
result_ = ', '.join(list1)
print(result_)
