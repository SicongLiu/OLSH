import math
import os
from openpyxl import load_workbook


def init_dict(top_k):
    index_time = dict()
    # for i in range(top_k):
    #     index_time[i + 1] = float(0)

    query_time = []
    if top_k == 25:
        length = 5
    else:
        length = 6
    for i in range(length):
        query_time.append(float(0))
    return index_time, query_time


def print_dict(dict_array):
    for i in range(len(dict_array)):
        if i % 3 == 0:
            print('\n')
        cur_dict = dict_array[i]
        # print("oops: ", max)
        print(cur_dict[1], cur_dict[2], cur_dict[5], cur_dict[10], cur_dict[max(cur_dict.keys())])
        # print(cur_dict[1], cur_dict[2], cur_dict[5], cur_dict[10], max(cur_dict, key=cur_dict.get))


def print_query_time_array(query_time_list_array_):
    for i in range(len(query_time_list_array_)):
        if i % 3 == 0:
            print('\n \n')
        if i % 9 == 0:
            print('\n ************************ \n ')
        cur_query_time_array = query_time_list_array_[i]
        print(cur_query_time_array)


def lines_contains_key(line_, dict_):
    if str(line_).strip().__len__() > 0:
        cur_lines = str(line_).strip().split('\t')
        for key in dict_.keys():
            if int(cur_lines[0]) == key:
                return 1
    return 0


file_name = '/Users/sicongliu/Desktop/ICDE2019_reply/red_4_4D_non200K_nohup.txt'
# file_name = '/Users/sicongliu/Desktop/non_4D_LSH_nohup.txt'
# file_name = '/Users/sicongliu/Desktop/4D_LSH_nohup.txt'
top_k = 25
f = open(file_name, 'r')
lines = f.readlines()
length = lines.__len__()

index_time_array = []
query_time_array = []
query_time_match = dict()
query_time_match[1] = 0
query_time_match[2] = 1
query_time_match[5] = 2
query_time_match[10] = 3
query_time_match[25] = 4

index_time, query_time = init_dict(top_k)

i = 0
indexing_time_flag = 0
layer_index_flag = 0
layer_index = 0
round_flag = 0

while i < length:
    if lines[i].__contains__("layer_index             = ") and layer_index_flag == 0:
        round_flag = 1
        layer_index_flag = 1
        print(lines[i])
        temp_line = lines[i + 4]
        print(temp_line)
        layer_index = layer_index + 1
    elif lines[i].__contains__("Indexing Time:") and lines[i].__contains__('Seconds') and layer_index_flag == 1:
        indexing_time_flag = 1
        cur_indexing_time = lines[i].split(' ')[2]
        print("indexing time", cur_indexing_time)
        if layer_index == 1:
            index_time[layer_index] = float(cur_indexing_time)
        else:
            index_time[layer_index] = float(index_time[layer_index - 1]) + float(cur_indexing_time)
            print("layer_index: ", layer_index, ", time: ", index_time[layer_index])

    elif lines[i].__contains__("Top-k		Time (ms)	Recall"):
        i = i + 1
        while not lines[i].__contains__('Top-k c-AMIP of Simple_LSH: ') and not lines[i].__contains__('Using threshold, layer index: ') and indexing_time_flag == 1:
            print(lines[i])
            flag = lines_contains_key(lines[i], query_time_match)
            if flag == 1:
                line_break = lines[i].split('\t')
                temp_key = int(line_break[0])
                temp_query_time = float(line_break[2])
                print(temp_query_time)
                temp_loc = query_time_match[temp_key]
                if temp_loc > 0:
                    query_time[temp_loc] = query_time[temp_loc] + temp_query_time
                else:
                    query_time[temp_loc] = temp_query_time
            i = i + 1
        indexing_time_flag = 0
        layer_index_flag = 0
    elif lines[i].__contains__('alg           = 12') and round_flag == 1:
        # aggregate
        print(index_time[layer_index])
        indexing_time_flag = 0
        layer_index_flag = 0
        layer_index = 0
        round_flag = 0
        index_time_array.append(index_time)
        query_time_array.append(query_time)
        # load into dict array
        index_time, query_time = init_dict(top_k)
    i = i + 1

print("======== indexing time ==========")
print_dict(index_time_array)

print("======== query time ==========")
print_query_time_array(query_time_array)