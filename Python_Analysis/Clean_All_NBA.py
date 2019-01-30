import os

dimensions = [7]
top_ks = [25]
types = ["log", "log_minus", "log_plus", "log_plus_plus", "uni"]
cardinality = 23338
query_count = 1000
ratio = 2
parameter_type = ["opt", "max", "uni"]
BASH_FILE_BASE_FOLDER = "../H2_ALSH/"

for k in range(dimensions.__len__()):
    dimension = dimensions[k]
    total_bash_file = BASH_FILE_BASE_FOLDER + "run_bash_set_cur_" + str(dimension) + 'D_' + str(cardinality) + '.sh'

    for m in range(types.__len__()):
        type_name = types[m]
        for i in range(top_ks.__len__()):
            top_k = top_ks[i]
            TEMPORAL_RESULT = "../H2_ALSH/temp_result_" + str(dimension) + "D_top" + str(top_k) + '_' + type_name + '_' + str(cardinality) + "/"
            if not os.path.exists(TEMPORAL_RESULT):
                continue
            else:
                os.system("rm " + TEMPORAL_RESULT + "*")

print("Done .\n")