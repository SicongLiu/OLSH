# script to generate .sh file for execution
# bash file includes execution of Ground Truth, LSH Scheme and Overall Performance

import os
import sys

types = ["log", "log_minus", "log_plus", "log_plus_plus", "uni"]

dimension = int(str(sys.argv[1]))
cardinality = int(str(sys.argv[2]))
budget_factor = int(str(sys.argv[3]))
top_k = int(str(sys.argv[4]))

budget = cardinality * budget_factor

for m in range(types.__len__()):
    type_name = types[m]

    TEMPORAL_RESULT = "../H2_ALSH/temp_result_" + str(dimension) + "D_top" + str(top_k) + "_budget_" + \
                      str(budget) + "_" + type_name + "_" + str(cardinality) + "/"

    if not os.path.exists(TEMPORAL_RESULT):
        continue
    else:
        os.system("rm " + TEMPORAL_RESULT + "run_*")
        os.system("rm " + TEMPORAL_RESULT + "overall_*")

print("Done .\n")