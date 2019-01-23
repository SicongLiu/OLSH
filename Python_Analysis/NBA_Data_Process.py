#!/usr/bin/env python
from __future__ import print_function
import os
import math
import sys
import numpy as np
import pandas as pd
import xlwt
import xlrd

# excel_path = '../NBA_Data/Oct_24_no_partial'

excel_directory = '../NBA_Data/Oct_24_with_partial/'
files = os.listdir(excel_directory)
files_xls = [f for f in files if f[-4:] == 'xlsx']
print(files_xls)
print(files_xls.__len__())

# MP -- 7
# FGA -- 9
# FTA -- 19
# TRB -- 23
# AST -- 24
# PF -- 28
# PTS -- 29
column_indices = [7, 9, 19, 23, 24, 28, 29]
dimension = 7
total_record_count = 0
total_data = []
for excel_file in files_xls:
    excel_file_path = os.path.join(excel_directory, excel_file)
    print(excel_file_path)
    workbook = xlrd.open_workbook(excel_file_path)

    worksheet = workbook.sheet_by_name("Sheet1")  # We need to read the data
    num_rows = worksheet.nrows  # Number of Rows
    num_cols = worksheet.ncols  # Number of Columns

    for row in range(1, num_rows):
        cur_record = []
        for c_index in range(0, column_indices.__len__()):
            column_index = column_indices[c_index]
            value = worksheet.cell_value(rowx=row, colx=column_index)
            if value == '' or str(value).isspace() or (c_index == 0 and float(value) < 10):
                continue
            # if c_index == 0 and (str(value).isspace() or str(value) == ''):
            #     continue
            # else:
            #     cur_record.append(value)
            cur_record.append(value)
        # if cur_record.__len__() > 0: # and cur_record.__len__() == dimension: # and int(cur_record[0]) >= 10:
        if cur_record.__len__() != dimension or str(cur_record[0]).isspace() or str(cur_record[0]) == "" \
                or '0' in cur_record or 0 in cur_record:
            continue
        else:
            total_data.append(cur_record)
            total_record_count = total_record_count + 1

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

file_name = "NBA_Data.txt"
temp_data = []
temp_data.append(dimension)
temp_data.append(total_record_count)
temp_data = np.asarray(temp_data)
np.savetxt(file_name, temp_data, delimiter=',', fmt='%i')

f_handle = open(file_name, 'ab')
np.savetxt(f_handle, scaled_points, fmt='%10.6f')
f_handle.close()

print("All Done .\n")
