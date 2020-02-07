import math
import os
from openpyxl import load_workbook


def init_dict(top_k):
    index_time = dict()
    index_mem = dict()
    query_mem = dict()
    # for i in range(top_k):
    #     index_time[i + 1] = float(0)

    query_time = []
    if top_k == 25:
        length = 5
    else:
        length = 6
    for i in range(length):
        query_time.append(float(0))
    return index_time, query_time, index_mem, query_mem


def print_dict(dict_array):
    for i in range(len(dict_array)):
        if i % 2 == 0:
            if i % 3 == 0:
                print('\n')
            cur_dict = dict_array[i]
            # print("oops: ", max)
            print(cur_dict[1], cur_dict[2], cur_dict[5], cur_dict[10], cur_dict[max(cur_dict.keys())])
            # print(cur_dict[max(cur_dict.keys())])
            # print(cur_dict[1], cur_dict[2], cur_dict[5], cur_dict[10], max(cur_dict, key=cur_dict.get))


def print_query_time_array(query_time_list_array_):
    for i in range(len(query_time_list_array_)):
        if i % 2 == 0:
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


# file_name = '/Users/sicongliu/Desktop/redundacy_6_stats/4D_red_6_nohup.txt'
# file_name = '/Users/sicongliu/Desktop/ICDE2019_reply/3D_red_4_nohup.txt'
# file_name = '/Users/sicongliu/Desktop/non_4D_LSH_nohup.txt'
# file_name = '/Users/sicongliu/Desktop/4D_LSH_nohup.txt'
# file_name = '/Users/sicongliu/Desktop/redundacy_4_stats_500k/500k_7D_nohup.txt'
# file_name = '/Users/sicongliu/Desktop/redundacy_4_stats_500k/500k_7D_nohup.txt'
# file_name = '/Users/sicongliu/Desktop/reverse_maths_0.3/4D_reverse_03_nohup.txt'
# file_name = '/Users/sicongliu/Desktop/redundacy_4_skyline_stats/4D_skyline_correlated_random_nohup.txt'
file_name = './layer_error_2D_nohup.txt'


top_k = 25
f = open(file_name, 'r')
lines = f.readlines()
length = lines.__len__()

index_time_array = []
query_time_array = []
index_mem_array = []
query_mem_array = []


anti_array = []
corr_array = []
random_array = []

query_time_match = dict()
query_time_match[1] = 0
query_time_match[2] = 1
query_time_match[5] = 2
query_time_match[10] = 3
query_time_match[25] = 4

index_time, query_time, index_mem, query_mem = init_dict(top_k)

i = 0
indexing_time_flag = 0
layer_index_flag = 0
layer_index = 0
round_flag = 0
recall_count = 0
dummy_count = 0
overall_flag = 0
while i < length:
    if lines[i].__contains__("alg           = 10") and layer_index_flag == 0:
        round_flag = 1
        layer_index_flag = 1
        # print(lines[i])
        temp_line = lines[i + 4]
        # print(temp_line)
        layer_index = layer_index + 1
    elif lines[i].__contains__("top_k             =") and layer_index_flag == 1:
        temp_line = lines[i].strip().split(' ')
        temp_len = len(temp_line)
        temp_topk = str(temp_line[temp_len - 1])
        cur_topk = int(temp_topk)
    elif lines[i].__contains__('alg           = 12') and round_flag == 1:
        i = i + 1
        # print(cur_topk)
        # while i < length and not lines[i].startswith('Top-t c-AMIP of Simple_LSH (overall): '):
        #     overall_flag = 1
        # while i < length and not (lines[i].startswith('   ' + str(cur_topk))) and not lines[i].startswith('   ' + str(cur_topk)) and round_flag == 1:
        #     # print(lines[i])
        while i < length and not lines[i].startswith('   ' + str(cur_topk))  and not lines[i].startswith('  ' + str(cur_topk)) and round_flag == 1:
            i = i + 1
        # print(lines[i])
        round_flag = 0
        dummy_count = 0
        if i < length:
            temp_line = lines[i].strip().split('\t')
            temp_recall = temp_line[2]
            print(temp_line)
            temp_cur_recall = float(temp_recall)
            # print(temp_line, temp_recall)
            # aggregate
            if recall_count == 0 :
                anti_array.append(temp_cur_recall)
                recall_count = recall_count + 1
            elif recall_count == 1:
                corr_array.append(temp_cur_recall)
                recall_count = recall_count + 1
            else:
                random_array.append(temp_cur_recall)
                recall_count = 0
            indexing_time_flag = 0
            layer_index_flag = 0
            layer_index = 0
            round_flag = 0
            cur_topk = -1
            index_time_array.append(index_time)
            query_time_array.append(query_time)

            index_mem_array.append(index_mem)
            query_mem_array.append(query_mem)

            # load into dict array
            index_time, query_time, index_mem, query_mem = init_dict(top_k)

    i = i + 1

print("======== indexing time ==========")
print(anti_array)