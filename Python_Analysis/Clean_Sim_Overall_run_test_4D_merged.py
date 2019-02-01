# script to generate .sh file for execution
# bash file includes execution of Ground Truth, LSH Scheme and Overall Performance

import os

data_type = ["anti_correlated", "correlated", "random"]
dimensions = [4]
top_ks = [10, 25, 50]
types = ["log", "log_minus", "log_plus", "log_plus_plus", "uni"]

card_excel = ['200k']
cardinality = [200000]

pot = 1

query_count = 1000
ratio = 2

parameter_path = '../H2_ALSH/parameters/'
parameter_type = ["opt", "max", "uni"]
BASE_FOLDER = "../H2_ALSH/qhull_data/Synthetic/"
BASH_FILE_BASE_FOLDER = "../H2_ALSH/"

for k in range(dimensions.__len__()):
    dimension = dimensions[k]
    for cc in range(cardinality.__len__()):
        total_bash_file = BASH_FILE_BASE_FOLDER + "run_bash_set_cur_" + str(dimension) + 'D_' + card_excel[cc] + '.sh'

        for m in range(types.__len__()):
            type_name = types[m]
            for i in range(top_ks.__len__()):
                top_k = top_ks[i]
                # parameter_dir = parameter_path + str(dimension) + "D_top" + str(top_k) + "_budget_" + str(budget)\
                #                     + "_" + type_name + "_" + card_excel[cc] + "/"
                # print(parameter_dir)
                # if not os.path.exists(parameter_dir):
                #     continue
                # else:
                BASH_FILE_FOLDER = BASH_FILE_BASE_FOLDER + "bash_set_" + str(dimension) + "D_top" + str(top_k) + \
                                   "_" + type_name + "_" + str(card_excel[cc]) + "/"
                TEMPORAL_RESULT = "../H2_ALSH/temp_result_" + str(dimension) + "D_top" + str(top_k) + \
                                  "_" + type_name + "_" + str(card_excel[cc]) + "/"
                TEMPORAL_RESULT_FOR_BASH = "./temp_result_" + str(dimension) + "D_top" + str(top_k) + "_" + \
                                           type_name + "_" + str(card_excel[cc]) + "/"
                if not os.path.exists(TEMPORAL_RESULT):
                    continue
                else:
                    # os.system("rm " + TEMPORAL_RESULT + "s*")
                    os.system("rm " + TEMPORAL_RESULT + "run_*")
                    os.system("rm " + TEMPORAL_RESULT + "overall_*")

print("Done .\n")