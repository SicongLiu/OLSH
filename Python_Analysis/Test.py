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


print(dim_75)
# f = open('dummy_test.txt', 'w')
# f.write(str(dim_75))
# f.close()
np.savetxt('dummy_test.txt', np.asarray(dim_75))

lines = np.loadtxt('dummy_test.txt')
print(lines)
print(type(lines))
print(lines.__len__())










