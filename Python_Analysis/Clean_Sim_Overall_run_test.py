# script to generate .sh file for execution
# bash file includes execution of Ground Truth, LSH Scheme and Overall Performance

import os

data_type = ["anti_correlated", "correlated", "random"]
budgets = ["1M", "10M"]
# dimensions = [4, 5]
# dimensions = [2, 3, 4, 5, 6]
dimensions = [4]
#  top_ks = [10, 25, 50]
top_ks = [25]
types = ["log", "log_minus", "log_plus", "log_plus_plus", "uni"]

# card_excel = ['100k', '200k', '500k', '1M', '15M', '2M']
# cardinality = [100000, 200000, 500000, 1000000, 1500000, 2000000]

card_excel = ['200k']
cardinality = [200000]

# card_excel = ['100k', '200k']
# cardinality = [100000, 200000]

excel_files = ["./4D.xlsx"]
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
            for j in range(budgets.__len__()):
                budget = budgets[j]
                for i in range(top_ks.__len__()):
                    top_k = top_ks[i]
                    parameter_dir = parameter_path + str(dimension) + "D_top" + str(top_k) + "_budget_" + str(budget)\
                                        + "_" + type_name + "_" + card_excel[cc] + "/"
                    print(parameter_dir)
                    if not os.path.exists(parameter_dir):
                        continue
                    else:
                        BASH_FILE_FOLDER = BASH_FILE_BASE_FOLDER + "bash_set_" + str(dimension) + "D_top" + str(top_k) + \
                                           "_budget_" + str(budget) + "_" + type_name + "_" + str(cardinality[cc]) + "/"
                        TEMPORAL_RESULT = "../H2_ALSH/temp_result_" + str(dimension) + "D_top" + str(top_k) + "_budget_" + \
                                          str(budget) + "_" + type_name + "_" + str(cardinality[cc]) + "/"
                        TEMPORAL_RESULT_FOR_BASH = "./temp_result_" + str(dimension) + "D_top" + str(top_k) + "_budget_" + \
                                                   str(budget) + "_" + type_name + "_" + str(cardinality[cc]) + "/"
                        os.system("rm " + TEMPORAL_RESULT + "s*")
                        os.system("rm " + TEMPORAL_RESULT + "r*")
                        os.system("rm " + TEMPORAL_RESULT + "o*")

print("Done .\n")