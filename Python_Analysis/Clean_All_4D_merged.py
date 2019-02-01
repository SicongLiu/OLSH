# script to generate .sh file for execution
# bash file includes execution of Ground Truth, LSH Scheme and Overall Performance

import os

data_type = ["anti_correlated", "correlated", "random"]

dimensions = [4]
top_ks = [10, 25, 50]

types = ["log", "log_minus", "log_plus", "log_plus_plus", "uni"]

# card_excel = ['100k', '200k', '500k', '1M', '15M', '2M']
# cardinality = [100000, 200000, 500000, 1000000, 1500000, 2000000]

card_excel = ['200k']
cardinality = [200000]

query_count = 1000
ratio = 2

parameter_path = '../H2_ALSH/parameters/'
parameter_type = ["opt", "max", "uni"]
BASH_FILE_BASE_FOLDER = "../H2_ALSH/"

for k in range(dimensions.__len__()):
    dimension = dimensions[k]
    for cc in range(cardinality.__len__()):
        total_bash_file = BASH_FILE_BASE_FOLDER + "run_bash_set_cur_" + str(dimension) + 'D_' + card_excel[cc] + '.sh'

        for m in range(types.__len__()):
            type_name = types[m]
            for i in range(top_ks.__len__()):
                top_k = top_ks[i]

                BASH_FILE_FOLDER = BASH_FILE_BASE_FOLDER + "bash_set_" + str(dimension) + "D_top" + str(top_k) + \
                                   "_" + type_name + "_" + str(card_excel[cc]) + "/"
                TEMPORAL_RESULT = "../H2_ALSH/temp_result_" + str(dimension) + "D_top" + str(top_k) + "_" + type_name \
                                  + "_" + str(card_excel[cc]) + "/"
                TEMPORAL_RESULT_FOR_BASH = "./temp_result_" + str(dimension) + "D_top" + str(top_k) + "_" + \
                                           type_name + "_" + str(card_excel[cc]) + "/"
                if not os.path.exists(TEMPORAL_RESULT):
                    continue
                else:
                    os.system("rm " + TEMPORAL_RESULT + "*")

print("Done .\n")