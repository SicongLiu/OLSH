#!/usr/bin/env python
from __future__ import print_function
import os
import math
import sys
import numpy as np
import pandas as pd
import xlwt
import xlrd

csv_file_path = '../HOUSE_Data/usa_2013_2017.csv'
save_data_file = "HOUSE_Data.txt"
# PROPINSR -- 6
# PROPTX99 -- 7
# COSTELEC -- 8
# COSTGAS -- 9
# COSTWATR -- 10
# COSTFUEL -- 11
import csv
column_indices = [6, 7, 8, 9, 10, 11]
dimension = 6

total_record_count = 0
row_count = 0
total_data = []
with open(csv_file_path, 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        cur_record = []
        if row_count > 0:
            for c_index in range(0, column_indices.__len__()):
                column_index = column_indices[c_index]

                value = row[column_index]
                # value = worksheet.cell_value(rowx=row, colx=column_index)
                if value == '' or str(value).isspace() or value == '0':
                    continue
                # if c_index == 0 and (str(value).isspace() or str(value) == ''):
                #     continue
                # else:
                #     cur_record.append(value)
                cur_record.append(float(value))
            # if cur_record.__len__() > 0: # and cur_record.__len__() == dimension: # and int(cur_record[0]) >= 10:
            if cur_record.__len__() != dimension or '0' in cur_record or 0 in cur_record:
                continue
            else:
                total_data.append(cur_record)
                total_record_count = total_record_count + 1
        row_count = row_count + 1
print("total number of record: " + str(total_record_count))


# normalize data
def normalize_data_dim(point_, scalors_):
    process_points = []
    for ii in range(dimension):
        process_points.append(point_[ii]/scalors_[ii])
    return process_points


scalors = []
for i in range(dimension):
    scalors.append(0)

for i in range(total_record_count):
    for ii in range(dimension):
        if total_data[i][ii] > scalors[ii]:
            scalors[ii] = total_data[i][ii]

scaled_points = []
for i in range(total_record_count):
    cur_point = normalize_data_dim(total_data[i], scalors)
    cur_point = np.asarray(cur_point)
    scaled_points.append(cur_point)

scaled_points = np.asarray(scaled_points)
temp_data = []
temp_data.append(dimension)
temp_data.append(total_record_count)
temp_data = np.asarray(temp_data)
np.savetxt(save_data_file, temp_data, delimiter=',', fmt='%i')

f_handle = open(save_data_file, 'ab')
np.savetxt(f_handle, scaled_points, fmt='%10.6f')
f_handle.close()
print("All Done .\n")
