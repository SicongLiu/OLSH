
import os

result_file_dir = '../H2_ALSH/'

result_type = ['with_threshold', 'without_threshold']

# get obj and hash count from bash_set
obj_hashsize_prefix = 'bash_set_'

# get candidate, recall and NDCG from temp_result
cand_recall_prefix = 'temp_result_'

# dimensions = [5]
dimensions = [4, 5]

card_file_name = ['1M', '500k', '100k', '200k']
card = [100000, 500000, 100000, 200000]
# card = [100000]

# optimized_tops = [10, 25]
optimized_tops = [25, 50]
# comp_types = ['opt', 'max', 'uni']
comp_types = ['opt', 'uni']

top_ks = [1, 2, 5, 10, 25, 50]
# budget = ['1M', '500k']
budget = ['1M']
types = ["log", "log_minus", "log_plus", "log_plus_plus", "uni"]
data_type = ["anti_correlated", "correlated", "random"]

over_reault = result_file_dir + 'all_aggregated_Oct_14.txt'
f = open(over_reault, 'w')

for dd in range(dimensions.__len__()):
    cur_dimension = dimensions[dd]
    for cc in range(card.__len__()):
        # cur_card_name = card_file_name[cc]
        cur_card = card[cc]
        for bb in range(budget.__len__()):
            cur_budget = budget[bb]
            for oo in range(optimized_tops.__len__()):
                cur_top_o = optimized_tops[oo]
                for tt in range(types.__len__()):
                    cur_type = types[tt]
                    for dt in range(data_type.__len__()):
                        cur_dt = data_type[dt]
                        for cr in range(result_type.__len__()):
                            cur_cr = result_type[cr]
                            for ct in range(comp_types.__len__()):
                                cur_ct = comp_types[ct]
                                obj_file_dir = result_file_dir + obj_hashsize_prefix + str(cur_dimension) + 'D_top' + \
                                            str(cur_top_o) + '_budget_' + cur_budget + '_' + cur_type + '_' + str(cur_card) + '/'
                                if not os.path.exists(obj_file_dir):
                                    continue

                                obj_file = obj_file_dir + 'cumsum_hashsize_obj_' + cur_ct + '_' + cur_dt + '_' + \
                                           str(cur_dimension) + '_' + str(cur_card) + '.txt'

                                f1 = open(obj_file, 'r')
                                lines = f1.readlines()
                                obj_s = lines[0].split(',')
                                # print(obj_s)
                                hash_s = lines[1].split(',')
                                # print(hash_s)

                                obj = []
                                hash = []
                                top_ks_length = -1
                                if cur_top_o == 10:
                                    top_ks_length = 4
                                elif cur_top_o == 25:
                                    top_ks_length = 5
                                else:
                                    top_ks_length = 6
                                for oh_index in range(top_ks_length):
                                    obj.append(int(obj_s[top_ks[oh_index] - 1]))
                                    hash.append(int(hash_s[top_ks[oh_index] - 1]))
                                f1.close()

                                temp_result_dir = result_file_dir + cand_recall_prefix + str(cur_dimension) + 'D_top' + \
                                            str(cur_top_o) + '_budget_' + cur_budget + '_' + cur_type + '_' + str(cur_card) + '/'

                                if not os.path.exists(temp_result_dir):
                                    continue

                                cand_size_list = []
                                for ii in range(top_ks_length):
                                    cand_result_file = temp_result_dir + 'run_test_' + cur_dt + '_' + str(cur_dimension) + '_' + \
                                                   str(cur_card) + '_' + cur_ct + '_' + cur_cr + '_top_' + str(top_ks[ii]) + '_candidate_size.txt'
                                    cand_size = 0
                                    f1 = open(cand_result_file, 'r')
                                    lines = f1.readlines()
                                    for jj in range(top_ks[ii]):
                                        cand_size += float(lines[jj].split(',')[0])
                                    # cand_size = float(cand_size)/float(top_ks[ii])
                                    cand_size = float(cand_size)
                                    cand_size_list.append(cand_size)
                                    f1.close()

                                overall_result_file = temp_result_dir + 'overall_run_test_' + cur_dt + '_' + str(
                                    cur_dimension) + '_' + str(cur_card) + '_' + cur_ct + '_' + cur_cr + '.txt'
                                # print(overall_result_file)
                                f1 = open(overall_result_file, 'r')
                                lines = f1.readlines()
                                recall = []
                                NDCG = []
                                # for ll in range(top_ks.__len__()):
                                for ll in range(top_ks_length):
                                    # print (lines[2*ll+1])
                                    ttt = lines[2*ll+1].split('\t')[0]
                                    # print(ttt)
                                    recall.append(float(lines[2*ll+1].split('\t')[1]))
                                    NDCG.append(float(lines[2*ll+1].split('\t')[2]))
                                # print(recall)
                                # print(NDCG)

                                # now we have
                                # recall NDCG cand_size_list obj hash

                                # cardinality, dimension, budget, top-10, log, anti_correlated, opt
                                spec_string = 'cardinality: ' + str(cur_card) + ', dimension: ' + str(cur_dimension) +\
                                              ',  budget: ' + str(cur_budget) + ', top-k: ' + str(cur_top_o) + ', type: ' \
                                              + cur_type + ', data: ' + cur_dt + ', compute type: ' + cur_ct
                                f.write(spec_string + '\n')
                                for ee in range(top_ks_length):
                                    f.write(str(recall[ee]) + ', ')
                                    f.write(str(NDCG[ee]) + ', ')
                                    f.write(str(cand_size_list[ee])  + ', ')
                                    f.write(str(obj[ee]) + ', ')
                                    f.write(str(hash[ee]) + ', ')
                                    f.write('\n')
                                f.write('\n')
                                f.write('\n')
f.close()
print('Done')