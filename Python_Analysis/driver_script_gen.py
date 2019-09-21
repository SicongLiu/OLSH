
import numpy as np

file_name = "./driver_script.sh"
bash_string = "#!/bin/bash"
cardinality = 100000
top_k = 25
raw_data_folder = "/Users/sliu104/Desktop/StreamingTopK/H2_ALSH/raw_data/Synthetic/"
output_folder = "/Users/sliu104/Desktop/StreamingTopK/H2_ALSH/qhull_data/Synthetic_test/"
dim_list = [17, 80, 26, 88, 90, 96, 57, 76, 70, 55, 54, 57, 61, 11, 38, 53, 94, 94, 92, 21, 23, 3, 45, 73, 41]
f = open(file_name, "w")
f.write(bash_string)
f.write("\n")
for ii in range(dim_list.__len__()):
    echo_string =  "echo \" running for " + str(dim_list[ii]) + "\""
    skyline_string = "./Skyline " + raw_data_folder + " random_" + str(dim_list[ii]) + "_" + str(cardinality) + " " + \
                     str(dim_list[ii]) + " " + str(cardinality) + " " + str(top_k) + " " + output_folder
    sleep_string = "sleep 3"
    f.write(echo_string + "\n")
    f.write(skyline_string + "\n")
    f.write(sleep_string + "\n \n")

f.close()
