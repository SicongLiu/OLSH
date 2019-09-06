import numpy as np
# x = np.array([3, 4])
# y = np.linalg.norm(x)
#
# yy = np.std(x)

import matplotlib.pyplot as plt

from  collections import Counter
a = [1,1,1,1,2,2,2,2,3,3,4,5,5]
b = [1,1,1,1,2,2,2,2,3,3,4,5,5]
counter_c = Counter()
counter_a = Counter(a)
counter_b = Counter(a)

counter_c = counter_c + counter_b
counter_c = counter_c + counter_a
print(counter_c)

plt.bar(counter_c.keys(), counter_c.values())
# print(type(counter))
# # Counter({1: 4, 2: 4, 3: 2, 5: 2, 4: 1})
# print(counter.values())
# # [4, 4, 2, 1, 2]
# print(counter.keys())
# # [1, 2, 3, 4, 5]


def dot(K, L):
   if len(K) != len(L):
      return 0

   return sum(i[0] * i[1] for i in zip(K, L))





data = [16 ,   78  , 251 ,  564  ,1121 , 1953,  3062,  4454 , 6330 , 8753, 11458, 15129, 18963,
        21103, 22608, 21815, 19633, 16395, 11703,  7625,  4206,  1868,   707,   173, 32]

#
# my_list = [3,2,56,4,32,4,7,88,4,3,4, 100]
# my_list = np.asarray(my_list)
# ooo = np.argsort((-my_list))
# print(ooo)
# print(list(ooo))
# print(type(ooo))
# print(type(list(ooo)))
# print(my_list[list(ooo)])
# bins = [0, 20, 40, 60, 80, 100]
# ttt = np.digitize(my_list, bins)
# print(ttt)
#
# arr = np.array([10, 20, 30, 40, 50])
# idx = [1, 0, 3, 4, 2]
# print(arr[idx])
# print(type(idx))
#
#
# query = [0.1, 0.2, 0.3, 0.4]
# print(query)
#
# chunks = 25
# top_k = 25
# data_folder = '/Users/sicongliu/Desktop/StreamingTopK/H2_ALSH/raw_data/Synthetic/'
# query_folder = '/Users/sicongliu/Desktop/StreamingTopK/H2_ALSH/query/'
# data_type = 'random_'
# dimension = 4
# cardinality = 200000
#
# file_name = data_folder + data_type + str(dimension) + '_' + str(cardinality) + '.txt'
# f = open(file_name, 'r')
# lines = f.readlines()
#
# cur_dim = int(lines[0])
# cur_card = int(lines[1])
# norm_list = []
# data_list = []
# for kk in range(cur_card):
#     current_data_record = np.fromstring(lines[kk + 2], dtype=float, sep=' ')
#     current_data_record = np.asarray(current_data_record)
#     data_list.append(current_data_record)
#     temp_norm = np.linalg.norm(current_data_record)
#     norm_list.append(temp_norm)
# f.close()
# norm_list = np.asarray(norm_list)
#
# inner_prod_list = []
# for jj in range(data_list.__len__()):
#     data_vector = data_list[jj]
#     inner_prod = dot(data_vector, query)
#     inner_prod_list.append(inner_prod)
#
# # sort index based on the dot product, then check which bin norm falls into
# inner_prod_list = np.asarray(inner_prod_list)
# reverse_sort_index = np.argsort((-inner_prod_list))
# top_k_index = reverse_sort_index[0: top_k]
#
# selected_norms = norm_list[list(top_k_index)]
# selected_inner_prod = inner_prod_list[list(top_k_index)]
# # match norm value into bin
#
# print(selected_norms)
# print(selected_inner_prod)
# print("Done")
#
#
