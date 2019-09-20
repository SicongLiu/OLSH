import numpy as np
# x = np.array([3, 4])
# y = np.linalg.norm(x)
#
# yy = np.std(x)

# import matplotlib.pyplot as plt
import math
from  collections import Counter

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

list1 = [1, 2, 3, 4, 5]
list2 = [2, 3, 4, 5, 6]
my_dict = {}
a = 1
b = 2
my_dict[a] = list1
my_dict[b] = list2

key = 1
temp = my_dict[key]
temp.extend(list2)
print(my_dict[key])
my_dict[b].extend(list1)
#
# print(my_dict)
#
# if key in my_dict.keys():
#     temp = list(my_dict[key])
#     print(temp)
#     print(temp.extend(list(list2)))
#     print(type(temp))
#     print(temp)
#     # print(temp.extend(list2))

# print(my_dict)
matrix = np.random.rand(10, 3)
print(matrix)
index = [0, 1, 2, 3]
print(matrix[index, 2])

for ii in my_dict.keys():
    my_dict[ii] = list(set(my_dict[ii]))
    print(my_dict[ii])