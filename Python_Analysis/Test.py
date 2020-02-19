import numpy as np
# x = np.array([3, 4])
# y = np.linalg.norm(x)
#
# yy = np.std(x)

import matplotlib.pyplot as plt
import math
from  collections import Counter
import random
from scipy.stats import beta

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
import re
def separate_string(input_string):
    items = []
    match = re.match(r"([a-z]+)([0-9]+)", input_string, re.I)
    if match:
        items = match.groups()
    return items

def colnum_string(n):
    string = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        string = chr(65 + remainder) + string
    return string

import string
def col2num(col):
    num = 0
    for c in col:
        if c in string.ascii_letters:
            num = num * 26 + (ord(c.upper()) - ord('A')) + 1
    return num



data_list_ = ['J6',  'J45', 'J51', 'J90']
k_ranges = ['E6',  'E45', 'E51', 'E90']
l_ranges_opt = ['F6', 'F45']
l_ranges_max = ['G6', 'G45']
l_ranges_uni = ['H6', 'H45']


# J, AA AQ
# Data_Types = ['anti_correlated', 'correlated', 'random']
def compute_data_list_start_end(data_type_index_, data_list, column_dist_):
    start_items_ = separate_string(data_list[0])
    start_letter_ = start_items_[0]
    start_num_ = start_items_[1]

    end_items_ = separate_string(data_list[1])
    end_letter_ = end_items_[0]
    end_num_ = end_items_[1]

    start_letter_integer_ = int(col2num(start_letter_))
    start_letter_integer_ = start_letter_integer_ + column_dist_ * data_type_index_
    start_letter_ = colnum_string(start_letter_integer_)
    data_list_start = start_letter_ + start_num_
    data_list_end = start_letter_ + end_num_

    return data_list_start, data_list_end


# both letter and integer row index change
def compute_ranges_start_end(column_shift, row_shift, ranges, row_dist_, column_dist_):
    range_start, range_end = compute_data_list_start_end(column_shift, ranges, column_dist_)
    range_column = separate_string(range_start)[0]
    range_row_start = separate_string(range_start)[1] # 6
    range_row_end = separate_string(range_end)[1] # 45
    row_span_ = int(range_row_end) - int(range_row_start)

    target_row_start = int(range_row_end) * row_shift + row_dist_ # 51
    target_row_end = target_row_start + row_span_
    k_ranges_temp_start = range_column + str(target_row_start)
    k_ranges_temp_end = range_column + str(target_row_end)

    return k_ranges_temp_start, k_ranges_temp_end


def compute_hash_cell(l_ranges_opt_temp_end, temp_row_dist, temp_column_dist):
    temp_column = separate_string(l_ranges_opt_temp_end)[0]
    temp_row = int(separate_string(l_ranges_opt_temp_end)[1])
    final_column = colnum_string(col2num(temp_column) + temp_column_dist)
    final_row = temp_row + temp_row_dist
    hash_used_cell = final_column + str(final_row)
    return hash_used_cell


import math



def millify(n):
    millnames = ['', 'K', 'M']
    n = float(n)
    millidx = max(0, min(len(millnames)-1, int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))

    return '{:.00f}{}'.format(n / 10**(3 * millidx), millnames[millidx])


list1 = [1, 4, 34, 34, 6, 8, 7, 32, 54, 346, 6, 10]
temp_counter = Counter(list1)
print(list(temp_counter.keys()))
# list1 = np.asarray(list1)
# print(list1)
#
# length = len(list1)
# cut_length = int(length * 0.5)
# list2 = list1[0:cut_length]
# print(list2)
#
# list3 = list1[cut_length: length]
# print(length, cut_length)
#
# print(list3)
#
# test_matrix_ = np.random.rand(5, 5)
# test_matrix_ = np.asarray(test_matrix_)
# print(test_matrix_)
#
# numrows = len(test_matrix_)
# numcols = len(test_matrix_[0])
#
# print(test_matrix_[:, 1])
# print(test_matrix_[1, :])



# data_list = np.random.rand(2,3)
#
# print(data_list)
#
# map(min, data_list)
# list(map(min, data_list))
# min_val = min(map(min, data_list))
#
# map(max, data_list)
# list(map(max, data_list))
# max_val = max(map(max, data_list))
#
# inter_val = max_val - min_val
#
# tt = (data_list - min_val)/max_val

# a = 5
# b = 2.8
#
# x = np.arange(0.01, 1, 0.01)
# y = beta.pdf(x, a, b)
# # plt.plot(x,y)
#
# plt.plot(x, y)
# plt.xticks([])
# plt.yticks([])
# # plt.plot(x, y1, "-", x, y2, "r--", x, y3, "g--")
# print('all done')


def Rand(start, end, num):
    res = []

    for j in range(num):
        res.append(random.randint(start, end))

    return res


# Driver Code
num = 100
start = 20
end = 40

tt1 = [13.22	13.143	13.112	13.088	12.925	12.665	12.585	12.564	12.604	12.523	12.38	12.203	12.28	12.148	12.054	11.902	11.694	11.899	11.726	11.675	11.603	11.417	11.308	11.332	11.226	11.186	11.183	11.128	11.213	11.203	11.189	11.071	10.926	11.016	11.292	11.279	11.09	10.869	10.932	11.169	10.948	10.445	10.557	10.952	11.224	11.328	11.47	11.509	11.367	11.179	11.265	11.514	11.718	11.662	11.576	11.571	11.596	11.591	11.777	11.537	11.732	11.746	11.599	11.67	11.752	11.816	11.99	11.949	11.93	11.989	11.881	11.736	11.681	11.572	11.467	11.415	11.27	11.075	10.845	10.648	10.361	10.154	10.263	10.408	10.402	10.45	10.473	10.497	10.674	10.811	10.696	10.805	10.784	10.716	10.477	10.181	9.8777	9.7337	9.5644	9.5866	9.7677	9.6725	9.3212	9.1632	9.251	9.2544	9.2467	9.2846	9.4712	9.5984	9.579	9.6073	9.8785	10.009	9.9588	9.7687	9.6711	9.6935	9.8867	10.07	10.055	10.134	9.9845	9.7635	9.7113	9.747	9.728	9.9885	10.156	10.044	10.075	10.061	10.041	10.092	10.215	10.414	10.238	9.9281	10.02	10.202	10.189	9.9026	9.7579	9.6531	9.6664	9.5344	8.9959	8.6176	8.6578	8.6456	8.3905	8.299	8.5126	8.7286	8.7514	8.6045	8.6331	8.7255	8.6784	8.4856	8.4839	8.6418	8.7825	8.851	8.8033	8.7384	8.6652	8.6403	8.628	8.6188	8.5351	8.4499	8.6279	8.8015	9.021	9.1852	9.221	9.0189	8.783	9.1865	9.4851	9.352	9.3877	9.8446	9.986	9.8122	9.5297	9.4267	9.6218	9.9874	10.013	9.756	9.7015	9.6698	9.5993	9.7737	9.8375	9.6994	9.7536	10.13	10.144	9.8986	9.8973	10.038	10.22	10.107	9.7976	9.7172	9.6511	9.2424	9.1909	9.2198	9.022	8.8127	8.5686	8.3934	8.5271	8.521	8.4603	8.6007	8.6684	8.7579	8.9113	8.7268	8.4975	8.4687	8.3856	8.3301	8.2097	8.1254	8.2837	8.6194	8.7847	8.7435	8.7763	8.7731	8.8322	8.9719	9.0309	9.1047	9.4419	9.6301	9.7444	9.676	9.4279	9.3153	9.2518	9.2807	9.5897	9.7531	9.5506	9.4412	9.5414	9.6675	9.6187	9.5827	9.6028	9.734	9.6334	9.5765	9.79	9.8996	9.9549	10.082	10.047	10.357	10.655	10.55	10.261	10.248	10.515	10.78	10.585	10.16	9.9475	10.166	10.26	10.201	10.024	9.4988	9.511	9.2311	9.1696	9.395	9.3804	9.3768	9.3476	9.3049	9.1485	9.1319	9.2539	9.3304	9.3964	9.5755	9.7382	9.7544	9.6897	9.7482	9.9297	9.8271	9.4885	9.5123	9.6101	9.7241	9.8389	9.8859	10.251	10.136	10.193	10.243	10.299	10.356	10.193	10.04	10.156	10.324	10.355	10.071	9.9317	10.009	10.048	10.046	9.9473	10.088	10.003	9.8002	10.273	9.9837	10.718	11.07	9.9824	10.469	10.87	11.184	9.8625	10.96	10.761	10.403	10.015	10.037	10.052	9.7137	9.292	8.8929	8.6556	8.5181	8.6194	8.3989	7.7117	8.0935	8.1201	8.0755	8.4006	8.1029	8.6836	8.8957	7.7166	8.5201	8.8775	8.5557]
tt2 = Rand(start, end, num)
tt3 = Rand(start, end, num)
ttt = [tt1, tt2, tt3]





print(ttt)
plt.plot(tt1)
plt.show()
print('Done')







