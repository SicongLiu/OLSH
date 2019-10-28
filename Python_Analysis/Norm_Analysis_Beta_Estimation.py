import os
import re
import sys
from openpyxl import load_workbook
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import math
from scipy.stats import beta


def compute_alpha_beta(input_ndarray_, min_index_, max_index_):
    sample_mean = np.mean(input_ndarray_)
    sample_var = np.var(input_ndarray_, ddof=1)
    x_bar = float(sample_mean - min_index_) / float(max_index_ - min_index_)
    var_bar = float(sample_var) / math.pow(float(max_index_ - min_index_), 2)
    alpha_ = x_bar * (x_bar * (1 - x_bar)/var_bar - 1)
    beta_ = (1 - x_bar) * (x_bar * (1 - x_bar)/var_bar - 1)

    return alpha_, beta_


freq_list = np.load('save_bin_array.npy')
freq_list = np.asarray(freq_list)
print(freq_list.__len__())
min_index = 1
max_index = 40 # max bin number

my_alpha, my_beta = compute_alpha_beta(freq_list, min_index, max_index)

# r = beta.rvs(my_alpha, my_beta, size=1000)
r = beta.rvs(my_alpha, my_beta, loc=min_index, scale=max_index - min_index, size=1000, random_state=None)
# plt.plot(r)
_ = plt.hist(r, bins='auto')  # arguments are passed to np.histogram
print('Done')










