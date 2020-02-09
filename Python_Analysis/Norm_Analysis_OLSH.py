import os
import re
import sys
from openpyxl import load_workbook
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import math
from scipy.stats import beta


def load_data(file_name):
    f = open(file_name, 'r')
    lines = f.readlines()
    cur_dim = int(lines[0])
    cur_card = int(lines[1])
    data_norm_list = []
    data_list = []
    for kk in range(cur_card):
        current_data_record = np.fromstring(lines[kk + 2], dtype=float, sep=' ')
        current_data_record = np.asarray(current_data_record)
        data_list.append(current_data_record)
        # temp_norm = float(format(np.linalg.norm(current_data_record), '.7f'))
        temp_norm = np.linalg.norm(current_data_record)
        data_norm_list.append(temp_norm)
    f.close()
    data_norm_list = np.asarray(data_norm_list)
    return data_list, data_norm_list


# plot norm distribution of different onion layers together
# data_types = ['anti_correlated', 'correlated', 'random']
data_types = ['random']
topk = 25
dim = 3
card = 200000
qhull_folder = '../H2_ALSH/qhull_data/Synthetic/'
raw_folder = '../H2_ALSH/raw_data/Synthetic/'

for data_type in data_types:
    # raw_data_file = raw_folder + data_type + '_' + str(dim) + '_' + str(card) + '.txt'
    # raw_data_list, raw_norm_list = load_data(raw_data_file)
    # _ = plt.hist(raw_norm_list, bins='auto')
    # plt.show()
    for i in range(topk):
        qhull_file = qhull_folder + data_type + '_' + str(dim) + '_' + str(card) + '_qhull_layer_' + str(i)
        cur_data_list, cur_norm_list = load_data(qhull_file)
        norm_mean = np.mean(np.asarray(cur_norm_list))
        print(norm_mean)
        _ = plt.hist(cur_norm_list, bins='auto')
        # plt.show()

print('Done')















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
temp_counter = Counter(freq_list)
print(temp_counter.keys())
print(freq_list.__len__())
min_index = 0
max_index = 40 # max bin number

my_alpha, my_beta = compute_alpha_beta(freq_list, min_index, max_index)

# r = beta.rvs(my_alpha, my_beta, size=1000)
r = beta.rvs(my_alpha, my_beta, loc=min_index, scale=max_index - min_index, size=1000000, random_state=None)


sample_bins_index = [22, 23, 24, 25, 26, 27, 28]
for i in range(sample_bins_index.__len__()):
    temp_val1 = beta.cdf(sample_bins_index[i], my_alpha, my_beta, loc=min_index, scale=max_index - min_index)
    print(temp_val1)

# _ = plt.hist(r, bins='auto')  # arguments are passed to np.histogram
print('Done')


# import pandas as pd
#
# ## convert your array into a dataframe
# df = pd.DataFrame (freq_list)
#
# ## save to xlsx file
#
# filepath = 'my_excel_file.xlsx'
#
# df.to_excel(filepath, index=False)
#
# print('Done')









