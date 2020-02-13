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
#
# # print(1.0 * sum(dim_1)/dim_1.__len__())
# # print(1.0 * sum(dim_10)/dim_10.__len__())
# # print(1.0 * sum(dim_15)/dim_15.__len__())
# # print(1.0 * sum(dim_20)/dim_20.__len__())
# # print(1.0 * sum(dim_25)/dim_25.__len__())
# # print(1.0 * sum(dim_50)/dim_50.__len__())
# # print(1.0 * sum(dim_75)/dim_75.__len__())
# list1 = [1, 2, 3, 4, 5]
# list2 = [6, 7, 8, 9]
#
# list3 = []
# list3.extend(list1)
# list3.extend(list2)
# print(list3)
#
# cur_min = 0
# cur_max = 10
#
# cur_index = 0
# while cur_index < cur_max:
#     print(cur_index)
#     cur_index = cur_index + 1
# bin_index

# tt = 25
# list_ = []
# for i in range(tt):
#     list_.append(i + 1)
# list_ = np.asarray(list_)
# tt = np.divide(list_, 10)
# print(tt)
#
import numpy as np
from scipy.stats import beta
import scipy.stats as stats
import matplotlib.pyplot as plt
from collections import Counter

import scipy
#


def calc_beta_dist(list_):
    mean_ = np.mean(list_)
    var_ = np.var(list_, ddof=1)

    alpha_ = ((1 - mean_)/var_ - 1/mean_) * mean_ * mean_
    beta_ = alpha_ * (1/mean_ - 1)
    return alpha_, beta_


def compute_alpha_beta(input_ndarray_, min_val_, max_val_):
    sample_mean = np.mean(input_ndarray_)
    sample_var = np.var(input_ndarray_, ddof=1)
    x_bar = float(sample_mean - min_val_) / float(max_val_ - min_val_)
    var_bar = float(sample_var) / math.pow(float(max_val_ - min_val_), 2)
    alpha_ = x_bar * (x_bar * (1 - x_bar)/var_bar - 1)
    beta_ = (1 - x_bar) * (x_bar * (1 - x_bar)/var_bar - 1)

    return alpha_, beta_

#
# ttt = [1, 2, 3, 4, 5]
# ttt = np.asarray(ttt)
# ttt = np.append(ttt, 10)
# print(ttt)
#
# xx = [0.0000000000010544000000000001, 0.19444000000000006, 0.14076, 0.14063999999999999, 0.11916, 0.11960000000000001, 0.091200000000000017, 0.056120000000000003, 0.02724, 0.0054000000000000003, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
#
# xx = np.asarray(xx)
# yy = np.array2string(xx, precision=5, separator=',', suppress_small=True)
#
# print(yy)
# # np.set_printoptions(suppress=True)
# # print(xx)
# # print(','.join(map(str, xx)))
#
# # xx = [0.27464, 0.30212, 0.23568000000000003, 0.13572000000000001, 0.039760000000000004, 0.01196, 0.00011999999999999999, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
# # xx = [0.47760000000000008, 0.37384000000000006, 0.13404000000000002, 0.014520000000000002, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ]
# xx = np.asarray(xx)
#
# xk = np.arange(25)
# cusm = stats.rv_discrete(name='cusm', values=(xk, xx))
# R = cusm.rvs(size=100000)
# tt = Counter(R)
# mc = np.digitize(R, xk)
# # print(mc)
# ma,  mb = compute_alpha_beta(mc, 1, 25)
#
# aaa = ma
#
#
# bbb = mb
# cc = 1
# dd = 25
# x = np.arange(cc, dd, 0.001)
# # fig, ax = plt.subplots(1, 1)
# # ax.plot(x, beta.pdf(x, aaa, bbb), 'r-', lw=5, alpha=0.6, label='beta pdf')
# y = beta.pdf(x, aaa, bbb,  loc=1, scale=25)
# plt.plot(x, y)
# plt.show()
#
# for ii in range(25):
#     if ii == 0:
#         print(beta.cdf(ii, aaa, bbb, loc=cc, scale=25))
#     else:
#         t1 = beta.cdf(ii, aaa, bbb, loc=cc, scale=25)
#         t2 = beta.cdf(ii + 1, aaa, bbb, loc=cc, scale=25)
#         print(t2 - t1)
#
# print('done').

tt = np.random.rand(5,3)
print(tt)
print("============")
ss = np.delete(tt, np.s_[-1:], axis=1)
print(ss.__len__())
print(ss.shape[0])

length = ss.shape[0]


