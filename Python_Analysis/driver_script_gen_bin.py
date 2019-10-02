
import numpy as np

file_name = "./driver_script.sh"
bash_string = "#!/bin/bash"
file_cardinality = 5000
cardinality = 500
top_k = 25
bin_count = 10
# raw_data_folder = "/Users/sliu104/Desktop/StreamingTopK/H2_ALSH/raw_data/Synthetic/"
raw_data_folder = "/Users/sliu104/Desktop/StreamingTopK/Python_Analysis/"
output_folder = "/Users/sliu104/Desktop/StreamingTopK/H2_ALSH/qhull_data/Synthetic_test/"
# dim_list = [17, 80, 26, 88, 90, 96, 57, 76, 70, 55, 54, 57, 61, 11, 38, 53, 94, 94, 92, 21, 23, 3, 45, 73, 41]
# dim_list = [0, 1, 4, 6, 7, 8, 11, 14, 16, 17, 18, 19, 21, 22, 26, 28, 31, 33, 34, 35, 36, 37, 40, 42, 45, 47, 50, 51, 52, 54, 55, 57, 59, 60, 63, 65, 69, 71, 75, 81, 82, 87, 89, 91, 92, 93, 94, 96, 98, 99]
# dim_list = [3, 9, 10, 13, 15, 23, 25, 29, 30, 38, 39, 46, 48, 49, 53, 58, 61, 62, 68, 72, 73, 76, 79, 83, 88]
# dim_list = [66, 5, 70, 41, 74, 80, 85, 86, 90, 95]
# dim_list = [32, 97, 2, 67, 64, 44, 43, 12, 77, 78, 56, 20, 24, 84, 27]
dim_list = list(range(0, 75))
f = open(file_name, "w")
f.write(bash_string)
f.write("\n")
for bb in range(bin_count):
    for ii in range(dim_list.__len__()):
        echo_string = "echo \" running for " + str(dim_list[ii]) + "\""
        skyline_string = "./Skyline " + raw_data_folder + " random_" + str(dim_list[ii]) + "_" + str(file_cardinality) + "_" + str(bb) + " " + \
                         str(dim_list[ii]) + " " + str(cardinality) + " " + str(top_k) + " " + output_folder
        sleep_string = "sleep 1"
        f.write(echo_string + "\n")
        f.write(skyline_string + "\n")
        f.write(sleep_string + "\n \n")

f.close()
