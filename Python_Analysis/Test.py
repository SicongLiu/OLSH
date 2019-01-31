import sys
import re
def colnum_string(n):
    string = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        string = chr(65 + remainder) + string
    return string


def compute_cell_index(column_index_start_, kk_, row_index_):
    column_index_num = column_index_start_ + kk_
    cs = colnum_string(column_index_num)
    cell_index_ = cs + str(row_index_)
    return cell_index_


def separate_string(input_string):
    items = []
    match = re.match(r"([a-z]+)([0-9]+)", input_string, re.I)
    if match:
        items = match.groups()
    return items


def compute_index(list_start_, top_m_):
    cell_index_ = []
    for start_ in list_start_:
        cell_index_.append(start_)
        ret_index = separate_string(start_)
        ret_ = ret_index[0] + str(int(ret_index[1]) + top_m_ - 1)
        cell_index_.append(ret_)
    return cell_index_


def computer_used_resource_index(start_, top_m_, count_):
    start_index_ = separate_string(start_)
    cell_index_ = []
    cell_index_.append(start_)
    first_ = start_index_[0] + str(int(start_index_[1]) + top_m_ - 1 + 8)
    cell_index_.append(first_)

    for i in range(2, count_):
        first_index = separate_string(first_)
        first_ = first_index[0] + str(int(first_index[1]) + top_m_ - 1 + 7)
        cell_index_.append(first_)
    return cell_index_


def topk_map(dimension_, cardinality_, type_, top_k_, map_, real_topk):
    temp_key_ = str(dimension_) + '_' + str(cardinality_) + '_' + type_ + '_' + top_k_
    map_[temp_key_] = real_topk
    return map_


def get_real_topk(dimension_, cardinality_, type_, top_k_, map_):
    temp_key_ = str(dimension_) + '_' + str(cardinality_) + '_' + type_ + '_' + top_k_
    real_topk = map_[temp_key_]
    return real_topk

# list_start = ['J6', 'J27', 'J47', 'J67', 'J87']
# top_m = 14
# ret_index = compute_index(list_start, top_m)
# print(ret_index)
#
# start = 'J6'
# resource_used = computer_used_resource_index(start, top_m, 5)
# print(resource_used)
#
# map = {}
# map['what'] = 1
# map[2] = 3
#
# print(map)
#
# print(map[2])
# print(map[3])

# row_index_start = [5, 15, 25, 35, 45]
# column_index_start = 2
# column_counts = 45
# row_counts = 6
#
# types = ["log", "log_minus", "log_plus", "log_plus_plus", "uni"]
# budgets = ["1M", "10M"]
# dimensions = [2]
#
# repeated_run = 10
# excel_folders = '../H2_ALSH/'
# column_counts = 45
# row_index = 5
#
# for ii in range(0, column_counts):
#     cell_index = compute_cell_index(column_index_start, ii, 5)
#     print(cell_index)


#
# def process_line(line_concate_):
#     processed_line_ = []
#     temp_arr = line_concate[line_concate.find("{") + 1:line_concate.find("}")].split(',')
#     for ii in range(len(temp_arr)):
#         processed_line_.append(int(temp_arr[ii].strip()))
#     return processed_line_
#
#
# # line_string = '27, 11, 7, 5, 4, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,' \
# #               ' 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1,1, 1, 1, 1'
# # line_list_ = line_string.split(',')
# # print(line_list_[0])
# read_lines = 3
# file_name = '4D_2M_Top50_anti.txt'
# f1 = open(file_name, 'r')
# line_count = 0
# bash_count = 0
# file_dict = {}
# line_concate = ''
# for line in f1.readlines():
#     line_count = line_count + 1
#     line_concate = line_concate + line.split('\n')[0].strip()
#     if line_count%read_lines == 0:
#         line_count = 0
#         file_dict[bash_count] = process_line(line_concate)
#         bash_count = bash_count + 1
#         # print(line_concate[line_concate.find("{")+1:line_concate.find("}")])
#         line_concate = ''
# f1.close()
# for ii in range(file_dict.__len__()):
#     print(file_dict[ii])
# import re
# str1 = 'Budget_10M_4D_top50_2M'
# str2 = '4D_Top50_2M'
# ret = str1.find(str2)
#
# if re.search(str2, str1, re.IGNORECASE):
#     print('yes')
#
# print(str1.find(str2))

tt1 = [[2, 3, 4], [1, 2, 3]]
tt2 = [[7,8,9], [2,3,4], [9,10,3]]
tt1.append(tt2)
print(tt1)
print(tt2[1:])

