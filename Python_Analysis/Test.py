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

# list1 = [0, 1, 4, 6, 7, 8, 11, 14, 16, 17, 18, 19, 21, 22, 26, 28, 31, 33, 34, 35, 36, 37, 40, 42, 45, 47, 50, 51, 52, 54, 55, 57, 59, 60, 63, 65, 69, 71, 75, 81, 82, 87, 89, 91, 92, 93, 94, 96, 98, 99]
# set1 = set(list1)
#
# print(set1)


dict1 = {}
dict3 = {}
dict3[4] = 5
dict1[1] = dict3
dict1[2] = 3
list1 = []
list1.__len__()
if dict1.__contains__(1):
    temp = dict1[1]
    temp[2] = 5
    print(dict1)
