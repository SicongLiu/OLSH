import numpy as np

# raw_data = [[1, 2], [3, 4], [4, 5], [2, 3]]
# raw_data = np.asarray(raw_data)
#
# query_data = [[1, 2, 3], [2, 3, 10], [5, 6, 9]]
# query_data = np.asarray(query_data)
#
# # tt = [[1, 2, 3], [2, 3, 10], [5, 6, 9]]
# # tt = np.asarray(tt)
# #
# # tt_index = [0, 1]
# # tt = np.delete(tt, tt_index, 0)
# # print("tt: " + str(tt))
#
#
# my_value = query_data[:, len(query_data[0])-1]
# print(my_value)
#
# query_data = query_data[:, 0 : len(query_data[0]) - 1]
# print("query data : ")
# print(query_data)
#
#
# test_list = []
# my_index = []
# for ii in range(len(query_data)):
#     my_row = np.where((raw_data == query_data[ii]).all(axis=1))[0]
#     if len(my_row) == 0:
#         my_value = np.delete(my_value, ii)
#         print("oops")
#         continue
#     print("my_row: " + str(my_row))
#
#     # my_index.append(my_row[0])
#     my_index.extend(my_row)
#     print(my_row[0])
#
# print("my index:" + str(my_index))
#
#
# file_name = 'basic_test.txt'
# f = open(file_name, 'w')
#
#
# # flush zip pair to file
# for idx, value in zip(my_index, my_value):
#     # write this to file
#     f.write(str(idx) + ' ' + str(value) + '\n')
# f.close()
#
# tt = []
# tt1 = list()
# tt1.append(2)
#
# print(tt1)
# my = [2, 3, 4]
# print(my)
#
# tt1 = tt1 + my
#
# tt = tt.append(my)
#
# print(tt1)

tt = list()
t1 = [1, 2, 3, 4]
# t2 = [2, 3, 56, 6,100]
# tt.append(t1)
# tt.append(t2)
# print(tt)
print(t1)
noise = np.random.normal(0,0.3,10)
print(noise)
print(t1)
t2 = t1 + t1
print(t2)
buckets = [0] * 10
print(buckets.__len__())

loc1 = [2, 5]
loc2 = [7, 9]
loc3 = [295, 320]
loc4 = [410, 430]

noise1 = np.random.normal(0,0.1,3)
noise2 = np.random.normal(0,0.1,35)
# noise3 = np.random.normal(0,0.1,25)
# noise4 = np.random.normal(0,0.1,20)
buckets[loc1[0]: loc1[1]] = noise1
# buckets[loc2[0]: loc2[1]] = noise2
# buckets[loc3[0]: loc3[1]] = noise3
# buckets[loc4[0]: loc4[1]] = noise4
print(buckets.__len__())
buckets[loc1[0]: loc1[1]] = noise1
print(buckets.__len__())