import numpy as np
import os
from pandas import DataFrame
import pandas as pd
import csv

num_of_dimension = 58
num_of_points = 1000 #42531
file_name = 'query_lsh_info.txt'

file_content = []
file_content.append(np.asarray(int(num_of_dimension)))
file_content.append(np.asarray(int(num_of_points)))
file_content = np.asarray(file_content)
np.savetxt(file_name, file_content, delimiter=',', fmt='%i')

data = []
with open("GPSI_Input.csv", "r") as f:
    reader = csv.reader(f, delimiter="\t")
    for i, line in enumerate(reader):
        if 0 < int(i) <= 1000:
            # print('line[{}] = {}'.format(i, line))
            line_content = line[0].split(',')
            line_content = np.asarray(line_content)
            line_content = line_content.astype(np.float)
            data.append(line_content)
            # print(line_content)
            # print(type(line_content))
            # print(line_content.size)#dimension
data = np.asarray(data)
f_handle = open(file_name, 'ab')
np.savetxt(f_handle, data, fmt='%10.6f')
f_handle.close()
print("All Done .\n")
