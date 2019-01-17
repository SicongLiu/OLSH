# script to generate .sh file for execution
# bash file includes execution of Ground Truth, LSH Scheme and Overall Performance

import math
import os


def cal_cumsum(input_num):
    i = 0
    count = 0
    while i <= input_num:
        count = count + i
        i = i + 1
    return count


# dimensions = [4, 5]
dimensions = [4]
#  top_ks = [10, 25, 50]
top_ks = [25]
top_k_interest = [1, 2, 5, 10, 25]
types = ["log", "log_minus", "log_plus", "log_plus_plus", "uni"]
# data_types = ['anti_correlated', 'correlated', 'random']
data_types = ['anti_correlated', 'correlated']
thresholds = ['with_threshold', 'without_threshold']
budgets = ['opt', 'uni', 'max']
thresholds = ['with_threshold', 'without_threshold']
card_excel = ['200k']
cardinality = [200000]

pot = 1
qn = 1000
# BASE_FOLDER = './'
BASE_FOLDER = '/Users/sicongliu/Desktop/StreamingTopK/H2_ALSH/'
for d in dimensions:
    for top_k in top_ks:
        for ttype in types:
            for card in cardinality:
                data_folder = BASE_FOLDER + 'temp_result_' + str(d) + 'D_top' + str(top_k) + '_budget_1M_' + \
                              str(ttype) + '_' + str(card) + '/'
                print(data_folder)
                for dtype in data_types:
                    for budget in budgets:
                        for threshold in thresholds:
                            anomaly_count_file = data_folder + 'anomaly_count_' + str(dtype) + '_' + str(d) + '_' + \
                                                 str(card) + '_' + str(budget) + '_' + str(threshold) + '.txt'
                            f3 = open(anomaly_count_file, 'w')
                            for ii in range(top_k_interest.__len__() - 1):
                                anomaly_count = 0
                                cur_topk = top_k_interest[ii]
                                next_topk = top_k_interest[ii + 1]
                                cur_file_name = data_folder + 'run_test_' + str(dtype) + '_' + str(d) + '_' + str(card) + '_' + \
                                            str(budget) + '_top_' + str(cur_topk) + '_' + str(threshold) + '.txt'
                                next_file_name = data_folder + 'run_test_' + str(dtype) + '_' + str(d) + '_' + str(card) + '_' + \
                                                str(budget) + '_top_' + str(next_topk) + '_' + str(threshold) + '.txt'

                                print('cur_file_name: ' + cur_file_name + ' \n')
                                print('next_file_name: ' + next_file_name + ' \n')
                                # check if next_file_name contains equal or better ones than cur_file_name element
                                # while they are not the same

                                # when loading data, each time read cur_topk amount of elements
                                cur_score_map = {}
                                q1 = 0
                                f1 = open(cur_file_name, 'r')
                                cur_lines = f1.readlines()
                                cur_count = cal_cumsum(cur_topk)
                                while q1 < qn * cur_count:
                                    cur_counter = 0
                                    cur_score_list = []
                                    while cur_counter < cur_count:
                                        cur_score = float(cur_lines[q1].split('\t')[d])
                                        cur_score_list.append(cur_score)
                                        cur_counter = cur_counter + 1
                                    cur_score_map[q1] = cur_score_list
                                    q1 = q1 + cur_count

                                f1.close()

                                # when loading data, each time read next_topk amount of elements
                                next_score_map = {}
                                q2 = 0
                                f2 = open(next_file_name, 'r')
                                next_lines = f2.readlines()
                                next_count = cal_cumsum(next_topk)
                                while q2 < qn * next_count:
                                    next_score_list = []
                                    next_counter = 0
                                    while next_counter < next_count:
                                        next_score = float(next_lines[q2].split('\t')[d])
                                        next_score_list.append(next_score)
                                        next_counter = next_counter + 1
                                    next_score_map[q2] = next_score_list
                                    q2 = q2 + next_count
                                f2.close()

                                # load score done, now compare values
                                for (k1, v1), (k2, v2) in zip(cur_score_map.items(), next_score_map.items()):
                                    # compare the cur_topk index from both lists
                                    index1 = sorted(range(len(v1)), key=lambda i: v1[i], reverse=True)[:cur_topk]
                                    # print(index1)

                                    index2 = sorted(range(len(v2)), key=lambda i: v2[i], reverse=True)[:cur_topk]
                                    # print(index2)

                                    if index1 != index2:
                                        anomaly_count = anomaly_count + 1

                                # output anormaly_count to file
                                f3.write('top_k: ' + str(cur_topk) + ', anomaly count: ' + str(anomaly_count) + ' \n')

                            f3.close()
print("Done .\n")