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

list1 = [0, 1, 4, 6, 7, 8, 11, 14, 16, 17, 18, 19, 21, 22, 26, 28, 31, 33, 34, 35, 36, 37, 40, 42, 45, 47, 50, 51, 52, 54, 55, 57, 59, 60, 63, 65, 69, 71, 75, 81, 82, 87, 89, 91, 92, 93, 94, 96, 98, 99]
# set1 = set(list1)
#
# print(set1)

import operator
import collections
# x = {75522.0: 0.234, 63276.0: 0.305, 80514.0: 0.98751, 53774.0: 0.03051, 49423.0: 0.03051, 55188.0: 0.03051, 31765.0: 0.03051, 57247.0: 0.03051, 18256.0: 0.03051, 32930.0: 0.03051, 9253.0: 0.03051, 20649.0: 0.03051, 72236.0: 0.03051, 40884.0: 0.03051, 72888.0: 0.03051, 62266.0: 0.03051, 50239.0: 0.03051, 48322.0: 0.03051, 10565.0: 0.03051, 7444.0: 0.0305, 74188.0: 0.03051, 92622.0: 0.03051, 18189.0: 0.03051, 80080.0: 0.03051, 41813.0: 0.03051, 82007.0: 0.03051, 43097.0: 0.03051, 80348.0: 0.03051, 14686.0: 0.03051, 45024.0: 0.03051, 70497.0: 0.03051, 98149.0: 0.0305, 31335.0: 0.03051, 83688.0: 0.03051, 86121.0: 0.03051, 59249.0: 0.03051, 21234.0: 0.03051, 53747.0: 0.0305, 67064.0: 0.0305, 32660.0: 0.03051, 40570.0: 0.03051, 55421.0: 0.03051}
# sorted_x = sorted(x.items(), key=lambda kv: kv[1], reverse=True)
# sorted_dict = collections.OrderedDict(sorted_x)
# print(sorted_x)
#
# ll = list(range(0, 100))
# print(ll)
# print(ll.__len__())


def histedges_equalN(x, nbin):
    npt = len(x)
    return np.interp(np.linspace(0, npt, nbin + 1),
                     np.arange(npt),
                     np.sort(x))
set1 = [0, 1, 4, 6, 7, 8, 11, 14, 16, 17, 18, 19, 21, 22, 26, 28, 31, 33, 34, 35, 36, 37, 40, 42, 45, 47, 50, 51, 52, 54, 55, 57, 59, 60, 63, 65, 69, 71, 75, 81, 82, 87, 89, 91, 92, 93, 94, 96, 98, 99]
set1 = list(set(set1))
# bin_aggregate, bin_edge = np.histogram(set1, bins=10)
# print(bin_edge)
# ret = np.digitize(set1, bin_edge)
# print(ret)
# result = np.where(ret == 11)
# print(result[0])


bin_edge = histedges_equalN(set1, 10)
ret = np.digitize(set1, bin_edge)
print(ret)