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
        if cur_record.__len__() != dimension or str(cur_record[0]).isspace() or str(cur_record[0]) == "":
            continue
        else:
            total_data.append(cur_record)
            total_record_count = total_record_count + 1

print("total number of record: " + str(total_record_count))


# normalize data
def compute_distance_with_origin(point, cur_dimension):
    distance = 0
    # print(point)
    for ii in range(cur_dimension):
        distance = distance + float(point[ii]) * float(point[ii])

    return math.sqrt(distance)


maxDistanceFromCenter = 0
minDistanceFromCenter = sys.float_info.max
scalors = []
for i in range(total_record_count):
    temp_distance = compute_distance_with_origin(total_data[i], dimension)
    if temp_distance > maxDistanceFromCenter:
        maxDistanceFromCenter = temp_distance
    if temp_distance < minDistanceFromCenter:
        minDistanceFromCenter = temp_distance
    if temp_distance == 0:
        print(total_data[i])
    scalors.append(temp_distance)

scaled_points = []
for i in range(total_record_count):
    factor = scalors[i]/maxDistanceFromCenter
    cur_point = []
    for j in range(dimension):
        cur_value = factor * (total_data[i][j] / scalors[i])
        cur_point.append(cur_value)
    scaled_points.append(cur_point)

# print for double check
maxDistanceFromCenter = 0
minDistanceFromCenter = sys.float_info.max
for i in range(total_record_count):
    cur_value = compute_distance_with_origin(scaled_points[i], dimension)
    if cur_value > maxDistanceFromCenter:
        maxDistanceFromCenter = cur_value
    if value < minDistanceFromCenter:
        minDistanceFromCenter = value
print("The maximum distance from  the center of the hipershere now is: " + str(maxDistanceFromCenter))
print("The minimum distance from  the center of the hipershere now is: " + str(minDistanceFromCenter))

file = open("NBA_Data.txt", "w")
file.write(str(dimension))
file.write("\n")
file.write(str(total_record_count))
file.write("\n")
# write file in text file
for i in range(total_record_count):
    s = "  ".join(map(str, scaled_points[i]))
    file.write(s)
    file.write("\n")
file.close()
print("All Done .\n")
