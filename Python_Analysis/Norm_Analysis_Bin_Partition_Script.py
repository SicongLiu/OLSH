import os
import re
import sys
from openpyxl import load_workbook
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import math
from scipy.stats import beta


def load_query(query_folder_, dimension_, is_stats_learn_):
    if is_stats_learn_:
        query_file_name = query_folder_ + 'query_' + str(dimension_) + 'D_stats_learn.txt'
    else:
        query_file_name = query_folder_ + 'query_' + str(dimension_) + 'D.txt'
    f = open(query_file_name, 'r')
    lines = f.readlines()
    cur_dim = int(lines[0])
    cur_card = int(lines[1])
    query_list = []
    for kk in range(cur_card):
        current_query_record = np.fromstring(lines[kk + 2], dtype=float, sep=' ')
        current_query_record = np.asarray(current_query_record)
        query_list.append(current_query_record)
    f.close()
    return np.asarray(query_list)


def delete_file(file_name_):
    os.system("rm " + file_name_)


def save_weight_to_file(weight_file_name, cdf_list_equal_width):
    np.savetxt(weight_file_name, np.asarray(cdf_list_equal_width))
    # f = open(weight_file_name, 'w')
    # f.write(cdf_list_equal_width)
    # f.close()


def ground_truth(data_type_, card_, dimension_, query_num_, is_stats_learn_):
    temp_file_name = SCRIPT_FOLDER + 'temp_ground_truth.sh'
    f = open(temp_file_name, 'w')
    f.write("#!/bin/bash \n")
    f.write("datatype=" + data_type_ + "\n")
    f.write("cardinality=" + str(card_) + "\n")
    f.write("d=" + str(dimension_) + "\n")
    f.write("qn=" + str(query_num_) + "\n")
    f.write("# ------------------------------------------------------------------------------ \n")
    f.write("#     Ground-Truth \n")
    f.write("# ------------------------------------------------------------------------------ \n")
    f.write("dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt \n")
    f.write(
        "tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth \n")
    if is_stats_learn_:
        f.write("qPath=./query/query_${d}D_stat_learn.txt \n")
    else:
        f.write("qPath=./query/query_${d}D.txt \n")
    f.write("oFolder=./result/result_${datatype}_${d}D_${cardinality} \n")

    f.write(" # ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts "
              "${oFolder}.mip \n")
    f.write(" # sleep 20 \n")
    f.close()
    os.system("sh " + temp_file_name)

    # after computing ground truth, delete this file
    os.system("rm " + temp_file_name)


def compute_alpha_beta(input_ndarray_, min_index_, max_index_):
    sample_mean = np.mean(input_ndarray_)
    sample_var = np.var(input_ndarray_, ddof=1)
    x_bar = float(sample_mean - min_index_) / float(max_index_ - min_index_)
    var_bar = float(sample_var) / math.pow(float(max_index_ - min_index_), 2)
    alpha_ = x_bar * (x_bar * (1 - x_bar)/var_bar - 1)
    beta_ = (1 - x_bar) * (x_bar * (1 - x_bar)/var_bar - 1)

    return alpha_, beta_


def compute_norm(input_file_, dimension_, card_):
    f = open(input_file_, 'r')
    lines = f.readlines()

    cur_dim = int(lines[0])
    cur_card = int(lines[1])

    assert cur_dim == dimension_
    assert cur_card == card_

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
    data_list = np.asarray(data_list)

    return data_norm_list, data_list


# return K_list
def save_bin_partition_on_file_equal_width(bin_count_, data_type_, dimension_, card_, digitize_index_, data_list):
    K_List = []
    for bb in range(bin_count_):
        temp_batch = []
        temp_batch.append(np.asarray(int(dimension_)))
        data_index_ = np.where(digitize_index_ == bb + 1)[0]  # those data save as bb
        temp_batch.append(np.asarray(int(data_index_.__len__())))

        # current_file = "./" + data_type_ + str(dimension_) + "_" + str(card_) + "_qhull_layer_" + str(bb)
        current_file = QHULL_OUTPUT_FOLDER + data_type_ + str(dimension_) + "_" + str(card_) + "_qhull_layer_" + str(bb)
        temp_batch = np.asarray(temp_batch)
        np.savetxt(current_file, temp_batch, delimiter=',', fmt='%i')

        temp_batch = []
        if len(data_index_) > 0:
            for dd in range(data_index_.__len__()):
                temp_batch.append(data_list[dd])
            K_List.append(data_index_.__len__())
        else:
            K_List.append(0)

        # separate metadata and data points, appending data points to metadata text saved on file
        f_handle = open(current_file, 'ab')
        np.savetxt(f_handle, temp_batch, fmt='%10.6f')
        f_handle.close()
    assert(sum(K_List) == card_)
    return K_List


def save_bin_partition_on_file_equal_depth(bin_count_, data_type_, dimension_, card_, split_array_):
    K_List = []
    for bb in range(bin_count_):
        current_data_list = split_array_[bb]
        temp_batch = []
        temp_batch.append(np.asarray(int(dimension_)))
        temp_batch.append(np.asarray(int(current_data_list.__len__())))
        current_file = QHULL_OUTPUT_FOLDER + data_type_ + str(dimension_) + "_" + str(
            card_) + "_qhull_layer_" + str(bb)

        temp_batch = np.asarray(temp_batch)
        np.savetxt(current_file, temp_batch, delimiter=',', fmt='%i')

        temp_batch = []
        if len(current_data_list) > 0:
            for dd in range(current_data_list.__len__()):
                temp_batch.append(current_data_list[dd])
            K_List.append(current_data_list.__len__())
        else:
            K_List.append(0)

        # separate metadata and data points, appending data points to metadata text saved on file
        f_handle = open(current_file, 'ab')
        np.savetxt(f_handle, temp_batch, fmt='%10.6f')
        f_handle.close()
    assert (sum(K_List) == card_)
    return K_List


# return bin_edge
def equal_width_bin_edges(dimension_, bin_count_):
    min_norm_ = 0
    max_norm_ = math.sqrt(dimension_)

    norm_range = float(max_norm_) - float(min_norm_)
    bin_range_ = norm_range / bin_count_

    bin_edges_ = []
    cur_norm = float(min_norm_)

    while float(cur_norm) <= float(max_norm_):
        bin_edges_.append(cur_norm)
        cur_norm = cur_norm + bin_range_

    print("bin len before process: " + str(bin_edges_.__len__()))
    if bin_edges_.__len__() == bin_count_ and bin_edges_[bin_edges_.__len__() - 1] < max_norm_:
        bin_edges_.append(bin_edges_[bin_edges_.__len__() - 1] + bin_range_)
    elif bin_edges_[bin_edges_.__len__() - 1] <= max_norm_:
        bin_edges_[bin_edges_.__len__() - 1] = max(max_norm_ + 0.0000001, bin_edges_[bin_edges_.__len__() - 1] + 0.0000001)

    print("bin len after process: " + str(bin_edges_.__len__()))

    return bin_edges_


def compute_bin_array(query_list_, query_num_, card_, data_list_, data_norm_list_, bins_, top_k_):
    save_bin_array = []
    total_counter = Counter()
    data_list_ = np.asarray(data_list_)
    for ii in range(query_num_):
        print("Query index: " + str(ii))
        cur_query = query_list_[ii]
        cur_query = np.asarray(cur_query)
        inner_prod_list = data_list_.dot(cur_query)

        inner_prod_list = np.asarray(inner_prod_list)
        reverse_sort_index = np.argsort((-inner_prod_list))
        top_k_index = reverse_sort_index[0: top_k_]

        selected_norms = data_norm_list_[list(top_k_index)]
        selected_inner_prod = inner_prod_list[list(top_k_index)]
        bin_count_array = np.digitize(selected_norms, bins_)
        save_bin_array.extend(bin_count_array)
        temp_counter = Counter(bin_count_array)
        total_counter = total_counter + temp_counter
    return np.asarray(save_bin_array), total_counter


def compute_cdf_equal_width(sample_bins_range_, my_alpha_, my_beta_, min_index_, max_index_):
    sample_bin_max_ = max(sample_bins_range_)
    cur_index_ = min_index_ + 1
    weight_cdf_ = []

    while cur_index_ <= max_index_:
        if cur_index_ > sample_bin_max_:
            temp_val1_ = beta.cdf(sample_bin_max_, my_alpha_, my_beta_, loc=min_index_, scale=max_index_ - min_index_)
            temp_val2_ = beta.cdf(cur_index_, my_alpha_, my_beta_, loc=min_index_, scale=max_index_ - min_index_)
            temp_val_ = temp_val2_ - temp_val1_
            weight_cdf_.append(temp_val_)
        else:
            temp_val_ = beta.cdf(cur_index_, my_alpha_, my_beta_, loc=min_index_, scale=max_index_ - min_index_)
            weight_cdf_.append(temp_val_)
        cur_index_ = cur_index_ + 1
    return np.asarray(weight_cdf_)


def compute_cdf_equal_depth(sample_bins_range_, my_alpha_, my_beta_, min_index_, max_index_):
    weight_cdf_ = []
    for ii in range(len(sample_bins_range_)):
        temp_bin_reading = sample_bins_range_[ii]
        temp_val_ = beta.cdf(temp_bin_reading, my_alpha_, my_beta_, loc=min_index_, scale=max_index_ - min_index_)
        weight_cdf_.append(temp_val_)
    return np.asarray(weight_cdf_)


def save_mathematica(card_List, cdf_weight_, top_k_, data_type_, dimension_, card_):
    function_str = "ret = queryRet" + str(top_k_) + "[count1, count, KList, fileName, hashTables];"
    save_data_file = SCRIPT_OUTPUT_FILE + "top_" + str(top_k_) + "_" + str(dimension_) + "D_" + str(card_) + ".txt"
    f = open(save_data_file, 'w')
    count = []
    count1 = []
    binWeight = []
    K_Log_List = []
    K_Log_Minus_List = []
    K_Log_Plus_List = []
    K_Log_Plus_Plus_List = []
    K_Log_Uni_List = []
    declare_string = data_type_ + "_" + str(dimension_) + "_" + str(card_)

    f.write("# ------------------------------------------------------------------------------ \n")
    f.write("#     " + declare_string + " \n")
    f.write("# ------------------------------------------------------------------------------ \n")
    # card_List same length as number of bins
    for kk in range(len(card_List)):
        binWeight.append(format(cdf_weight_[kk], '.10f'))
        count1.append(max(card_List[kk], 1))
        count.append(format(float(max(card_List[kk], 1))/float(sum(card_List)), '.10f'))

        k_log = 1
        if card_List[kk] == 0:
            k_log = 1
        else:
            k_log = max(math.ceil(math.log(card_List[kk], 2)), 1)
        k_log_minus = max(k_log - 3, 1)
        k_log_plus = k_log + 3
        k_log_plus_plus = k_log + 6

        K_Log_List.append(k_log)
        K_Log_Minus_List.append(k_log_minus)
        K_Log_Plus_List.append(k_log_plus)
        K_Log_Plus_Plus_List.append(k_log_plus_plus)

    k_log_max = max(K_Log_List)
    for m in range(len(card_List)):
        K_Log_Uni_List.append(k_log_max)
    hashTables = gen_hash_tables(top_k_)
    f.write("hashTables = List[" + hashTables + "] \n")
    f.write("binWeight = List[" + str(', '.join(map(str, binWeight))) + "] \n")
    f.write("count = List[" + str(', '.join(map(str, count))) + "]; \n")
    f.write("count1 = List[" + str(', '.join(map(str, count1))) + "]; \n")

    f.write("KList = List" + str(K_Log_List) + "; \n")
    f.write(function_str + "\n")

    f.write("KList = List" + str(K_Log_Minus_List) + "; \n")
    f.write(function_str + "\n")

    f.write("KList = List" + str(K_Log_Plus_List) + "; \n")
    f.write(function_str + "\n")

    f.write("KList = List" + str(K_Log_Plus_Plus_List) + "; \n")
    f.write(function_str + "\n")

    f.write("KList = List" + str(K_Log_Uni_List) + "; \n")
    f.write(function_str + "\n")

    f.write("\n \n \n")
    f.close()


def gen_hash_tables(top_k_):
    hashTables = []
    start_char = 'a'
    temp_prefix = ''
    for ii in range(top_k_):
        temp_index = ii
        start_char_length = float(temp_index) / 26
        start_char_diff = temp_index % 26
        temp_char = chr(ord(start_char) + start_char_diff)

        if math.floor(start_char_length) > temp_prefix.__len__():
            temp_prefix = temp_prefix + 'a'
        temp_char = temp_prefix + temp_char
        hashTables.append(temp_char)

    result_ = ', '.join(hashTables)
    return result_


def compute_bin_percentage(data_norm_list_, bin_count_, bin_edges_equal_width_):
    partition_norm_list = np.array_split(data_norm_list_, bin_count_)
    bin_percentage = []
    for ii in range(bin_count_):
        temp_norm = partition_norm_list[ii]
        max_temp = max(partition_norm_list[ii])
        max_temp_index = -1
        left_pivot = -1
        right_pivot = -1
        for jj in range(bin_edges_equal_width_.__len__()):
            if max_temp < bin_edges_equal_width_[jj]:
                max_temp_index = jj - 1
                left_pivot = jj - 1
                right_pivot = jj
                break

        temp_range = bin_edges_equal_width_[right_pivot] - bin_edges_equal_width_[left_pivot]
        temp_add_on = max_temp - bin_edges_equal_width_[left_pivot]
        temp_percentage = float(temp_add_on) / float(temp_range)
        temp_bin_percentage = jj - 1 + temp_percentage
        bin_percentage.append(temp_bin_percentage)

    print(bin_percentage)
    return np.asarray(bin_percentage)


def equal_depth_partition_data(input_file_, dimension_, card_, bin_count_, data_type_, data_gen_type_, query_list_, query_num_, top_k_, my_alpha_, my_beta_, bin_edges_equal_width_):
    data_norm_list, data_list = compute_norm(input_file_, dimension_, card_)
    max_norm = max(data_norm_list)
    min_norm = min(data_norm_list)
    sorted_norm_index = np.argsort(data_norm_list)
    # re-order data_list based on sorted_norm_index
    data_norm_list = [data_norm_list[i] for i in sorted_norm_index]
    data_list = [data_list[i] for i in sorted_norm_index]

    split_array = np.array_split(data_list, bin_count_)

    # following for hashing in the later phase
    # data_type_ = data_type_ + 'equal_depth_'
    data_type_ = data_type_ + data_gen_type_
    card_List = save_bin_partition_on_file_equal_depth(bin_count_, data_type_, dimension_, card_, split_array)

    sample_bins_range_ = compute_bin_percentage(data_norm_list, bin_count_, bin_edges_equal_width_)
    min_index_ = 0
    max_index_ = bin_count_  # max bin number
    weight_cdf_list_ = compute_cdf_equal_depth(sample_bins_range_, my_alpha_, my_beta_, min_index_, max_index_)

    # save Mathematica format to file
    save_mathematica(card_List, weight_cdf_list_, top_k_, data_type_, dimension_, card_)
    return np.asarray(weight_cdf_list_)


def compute_norm_range(bin_edges_equal_width_, bin_index_):
    low_end = math.floor(bin_index_)
    upper_end = math.ceil(bin_index_)
    low_norm = bin_edges_equal_width_[low_end]
    upper_norm = bin_edges_equal_width_[upper_end]
    target_norm = low_norm + (bin_index_ - low_end) * (upper_norm - low_norm)
    return target_norm


def equal_depth_partition_data_equal_weight(input_file_, dimension_, card_, bin_count_, data_type_, data_gen_type_, query_list_, query_num_, top_k_, my_alpha_, my_beta_, bin_edges_equal_width_):
    data_norm_list, data_list = compute_norm(input_file_, dimension_, card_)
    max_norm = max(data_norm_list)
    min_norm = min(data_norm_list)
    sorted_norm_index = np.argsort(data_norm_list)
    data_type_ = data_type_ + data_gen_type_
    # re-order data_list based on sorted_norm_index
    data_norm_list = [data_norm_list[i] for i in sorted_norm_index]
    data_list = [data_list[i] for i in sorted_norm_index]

    data_list = np.asarray(data_list)
    data_norm_list = np.asarray(data_norm_list)
    prob_step = float(1)/float(bin_count_)
    min_index_ = 0
    max_index_ = bin_count_  # max bin number

    K_List = []
    norm_partition_bin_list = []
    temp_norm_list = []
    current_prob = prob_step
    prob_list = []
    previous_norm = 0

    for ii in range(bin_count_):
        temp_bin_mark = beta.ppf(min(current_prob, 1), my_alpha_, my_beta_, loc=min_index_, scale=max_index_ - min_index_)
        norm_threshold = compute_norm_range(bin_edges_equal_width_, temp_bin_mark)
        target_index = np.where(np.logical_and(data_norm_list > previous_norm, data_norm_list <= norm_threshold))[0]
        previous_norm = norm_threshold

        # save those data on file
        temp_data_bash = data_list[target_index]
        temp_data_bash_size = temp_data_bash.__len__()

        if temp_data_bash_size > 0:
            K_List.append(temp_data_bash_size)
        else:
            K_List.append(0)

        current_file = QHULL_OUTPUT_FOLDER + data_type_ + str(dimension_) + "_" + str(
            card_) + "_qhull_layer_" + str(ii)

        temp_batch = []
        temp_batch.append(np.asarray(int(dimension_)))
        temp_batch.append(np.asarray(int(temp_data_bash_size)))
        temp_batch = np.asarray(temp_batch)
        np.savetxt(current_file, temp_batch, delimiter=',', fmt='%i')

        temp_data_bash = np.asarray(temp_data_bash)
        f_handle = open(current_file, 'ab')
        np.savetxt(f_handle, temp_data_bash, fmt='%10.6f')
        f_handle.close()

        norm_partition_bin_list.append(current_prob)
        temp_norm_list.append(temp_bin_mark)
        prob_list.append(current_prob)
        current_prob = current_prob + prob_step

    assert (sum(K_List) == card_)

    print('prob list', prob_list)

    # save Mathematica format to file
    save_mathematica(K_List, prob_list, top_k_, data_type_, dimension_, card_)
    return K_List


# partition the data based on the norm, save on file
def equal_width_partition_data(input_file_, dimension_, card_, bin_count_, data_type_, data_gen_type_, query_list_, query_num_, top_k_):
    data_norm_list, data_list = compute_norm(input_file_, dimension_, card_)
    max_norm = max(data_norm_list)
    min_norm = min(data_norm_list)

    # equal width
    bin_edge = equal_width_bin_edges(dimension_, bin_count_)

    print("min norm: " + str(min_norm))
    print("max norm: " + str(max_norm))
    print("bin edges: " + str(bin_edge))

    digitize_index_ = np.digitize(data_norm_list, bin_edge)

    # once having those bin_array, learn beta distribution through Counter() from each query
    bin_array_, total_counter_ = compute_bin_array(query_list_, query_num_, card_, data_list, data_norm_list, bin_edge, top_k_)
    min_index_ = 0
    max_index_ = bin_count_  # max bin number

    # learn beta distribution parameter
    my_alpha_, my_beta_ = compute_alpha_beta(bin_array_, min_index_, max_index_)
    sample_bins_range_ = list(total_counter_.keys())
    print(total_counter_)
    weight_cdf_list_ = compute_cdf_equal_width(sample_bins_range_, my_alpha_, my_beta_, min_index_, max_index_)

    # following for hashing in the later phase
    # data_type_ = data_type_ + 'equal_width_'
    data_type_ = data_type_ + data_gen_type_
    card_List = save_bin_partition_on_file_equal_width(bin_count_, data_type_, dimension_, card_, digitize_index_, data_list)

    # save Mathematica format to file
    save_mathematica(card_List, weight_cdf_list_, top_k_, data_type_, dimension_, card_)
    return np.asarray(weight_cdf_list_),  my_alpha_, my_beta_, bin_edge


SCRIPT_FOLDER = "../H2_ALSH/"
SCRIPT_OUTPUT_FILE = "../H2_ALSH/parameters/Mathematica_norm_bin_partition_Parameters_"
QHULL_OUTPUT_FOLDER = '/Users/sicongliu/Desktop/StreamingTopK/H2_ALSH/qhull_data/Synthetic/'
DATA_FOLDER = '/Users/sicongliu/Desktop/StreamingTopK/H2_ALSH/raw_data/Synthetic/'
QUERY_FOLDER = '/Users/sicongliu/Desktop/StreamingTopK/H2_ALSH/query/'
GROUNDTRUEH_FOLDER = "../H2_ALSH/result/"

top_k_ = 25
dimension_ = 300
card_ = 17770
bin_count_ = 40
query_num_ = 100

# use the query stats learn, for the following
is_stats_learn = 1
query_list_ = load_query(QUERY_FOLDER, dimension_, is_stats_learn)

# compute ground truth
data_type = 'random_'
data_gen_type = 'EW_'
ground_truth(data_type + data_gen_type, card_, dimension_, query_num_, is_stats_learn)

input_file_ = DATA_FOLDER + data_type + str(dimension_) + '_' + str(card_) + '.txt'
cdf_list_equal_width, my_alpha_, my_beta_, bin_edges_equal_width_ = equal_width_partition_data(input_file_, dimension_, card_, bin_count_, data_type, data_gen_type, query_list_, query_num_, top_k_)
# save weight to file
weight_file_name = './' + str(dimension_) + '_' + str(card_) + '_' + str(bin_count_) + '_' + 'top_' + str(top_k_) + '_EW.txt'
save_weight_to_file(weight_file_name, cdf_list_equal_width)

data_gen_type = 'ED_card_'
cdf_list_equal_depth = equal_depth_partition_data(input_file_, dimension_, card_, bin_count_, data_type, data_gen_type, query_list_, query_num_, top_k_, my_alpha_, my_beta_, bin_edges_equal_width_)
# save weight to file
weight_file_name = './' + str(dimension_) + '_' + str(card_) + '_' + str(bin_count_) + '_' + 'top_' + str(top_k_) + '_ED_card.txt'
save_weight_to_file(weight_file_name, cdf_list_equal_depth)

data_gen_type = 'ED_prob_'
K_List = equal_depth_partition_data_equal_weight(input_file_, dimension_, card_, bin_count_, data_type, data_gen_type, query_list_, query_num_, top_k_, my_alpha_, my_beta_, bin_edges_equal_width_)

# delete ground truth with query_stats_learn from regular queries for testing
ground_trouth_file = GROUNDTRUEH_FOLDER + 'result_' + data_type + data_gen_type + str(dimension_) + '_D_' + str(card_) + '.mip'
delete_file(ground_trouth_file)

is_stats_learn = 0
query_list_ = load_query(QUERY_FOLDER, dimension_, is_stats_learn)
ground_truth(data_type + data_gen_type, card_, dimension_, query_num_, is_stats_learn)

print('Done')