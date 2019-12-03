# script to generate .sh file for execution
# bash file includes execution of Ground Truth, LSH Scheme and Overall Performance

import os
import sys


budgets = ["35540"]

top_ks = [10, 25, 50]

types = ["log", "log_minus", "log_plus", "log_plus_plus", "uni"]

card_excel = ['17770']
cardinality = [17770]

BASH_FILE_BASE_FOLDER = "../H2_ALSH/"

dimension = str(sys.argv[1])

for cc in range(cardinality.__len__()):
    total_bash_file = BASH_FILE_BASE_FOLDER + "run_bash_set_cur_" + str(dimension) + 'D_' + card_excel[cc] + '.sh'

    for m in range(types.__len__()):
        type_name = types[m]
        for j in range(budgets.__len__()):
            budget = budgets[j]
            for i in range(top_ks.__len__()):
                top_k = top_ks[i]

                BASH_FILE_FOLDER = BASH_FILE_BASE_FOLDER + "bash_set_" + str(dimension) + "D_top" + str(top_k) + \
                                   "_budget_" + str(budget) + "_" + type_name + "_" + str(cardinality[cc]) + "/"
                TEMPORAL_RESULT = "../H2_ALSH/temp_result_" + str(dimension) + "D_top" + str(top_k) + "_budget_" + \
                                  str(budget) + "_" + type_name + "_" + str(cardinality[cc]) + "/"
                TEMPORAL_RESULT_FOR_BASH = "./temp_result_" + str(dimension) + "D_top" + str(top_k) + "_budget_" + \
                                           str(budget) + "_" + type_name + "_" + str(cardinality[cc]) + "/"
                if not os.path.exists(TEMPORAL_RESULT):
                    continue
                else:
                    os.system("rm " + TEMPORAL_RESULT + "*")

print("Done .\n")