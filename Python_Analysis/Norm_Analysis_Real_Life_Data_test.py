import os
import re
import sys
from openpyxl import load_workbook
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import math
from scipy.stats import beta


dimension = 300 # yahoo
data_type = 'random'
cardinality = 17770
data_folder = "/Users/sicongliu/Desktop/StreamingTopK/H2_ALSH/raw_data/Synthetic/"

file_name = data_folder + data_type + '_' + str(dimension) + '_' + str(cardinality) + '.txt'
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
    temp_norm = np.linalg.norm(current_data_record)
    data_norm_list.append(float("{0:.5f}".format(temp_norm)))

f.close()
data_norm_list = np.asarray(data_norm_list)
data_list = np.asarray(data_list)
min_norm = min(data_norm_list)
max_norm = max(data_norm_list)
mean_norm = np.mean(data_norm_list)
std_norm = np.std(data_norm_list)

print('min_norm =', min_norm, ', max_norm = ', max_norm, ', mean_norm = ', max_norm, ', std_norm = ', std_norm)

_ = plt.hist(data_norm_list)  # arguments are passed to np.histogram
plt.xlabel('norm_values')
plt.ylabel('frequency')

print('Done')
