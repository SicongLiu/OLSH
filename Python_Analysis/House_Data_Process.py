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
                if value == '' or str(value).isspace():
                    continue
                # if c_index == 0 and (str(value).isspace() or str(value) == ''):
                #     continue
                # else:
                #     cur_record.append(value)
                cur_record.append(value)
            # if cur_record.__len__() > 0: # and cur_record.__len__() == dimension: # and int(cur_record[0]) >= 10:
            if cur_record.__len__() != dimension or '0' in cur_record:
                continue
            else:
                total_data.append(cur_record)
                total_record_count = total_record_count + 1
        row_count = row_count + 1
print("total number of record: " + str(total_record_count))
#
# # save to excel format
#
# # data since 2000
# excel_file_path = '../HOUSE_Data/usa_00004.xlsx'
# sheetname = "usa_00004"
# save_data_file = "HOUSE_Data.txt"
#
#
#
#
#
# column_indices = [5, 6, 7, 8, 9, 10]
#
# total_record_count = 0
# total_data = []
# workbook = xlrd.open_workbook(excel_file_path)
# worksheet = workbook.sheet_by_name(sheetname)  # We need to read the data
# num_rows = worksheet.nrows  # Number of Rows
# num_cols = worksheet.ncols  # Number of Columns
#
# for row in range(1, num_rows):
#     cur_record = []
#     for c_index in range(0, column_indices.__len__()):
#         column_index = column_indices[c_index]
#         value = worksheet.cell_value(rowx=row, colx=column_index)
#         if value == '' or str(value).isspace() or (c_index == 0 and float(value) < 10):
#             continue
#         # if c_index == 0 and (str(value).isspace() or str(value) == ''):
#         #     continue
#         # else:
#         #     cur_record.append(value)
#         cur_record.append(value)
#     # if cur_record.__len__() > 0: # and cur_record.__len__() == dimension: # and int(cur_record[0]) >= 10:
#     if cur_record.__len__() != dimension or str(cur_record[0]).isspace() or str(cur_record[0]) == "" or '0' in \
#             cur_record or 0 in cur_record:
#         continue
#     else:
#         total_data.append(cur_record)
#         total_record_count = total_record_count + 1
#
# print("total number of record: " + str(total_record_count))


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
        cur_value = factor * (float(total_data[i][j]) / float(scalors[i]))
        cur_point.append(cur_value)
    cur_point = np.asarray(cur_point)
    scaled_points.append(cur_point)

scaled_points = np.asarray(scaled_points)
# print for double check
maxDistanceFromCenter = 0
minDistanceFromCenter = sys.float_info.max
for i in range(total_record_count):
    cur_value = compute_distance_with_origin(scaled_points[i], dimension)
    if cur_value > maxDistanceFromCenter:
        maxDistanceFromCenter = cur_value
    if cur_value < minDistanceFromCenter:
        minDistanceFromCenter = cur_value
print("The maximum distance from  the center of the hipershere now is: " + str(maxDistanceFromCenter))
print("The minimum distance from  the center of the hipershere now is: " + str(minDistanceFromCenter))

temp_data = []
temp_data.append(dimension)
temp_data.append(total_record_count)
temp_data = np.asarray(temp_data)
np.savetxt(save_data_file, temp_data, delimiter=',', fmt='%i')

f_handle = open(save_data_file, 'ab')
np.savetxt(f_handle, scaled_points, fmt='%10.6f')
f_handle.close()

# file = open(save_data_file, "w")
# file.write(str(dimension))
# file.write("\n")
# file.write(str(total_record_count))
# file.write("\n")
# # write file in text file
# for i in range(total_record_count):
#     s = "  ".join(map(str, scaled_points[i]))
#     file.write(s)
#     file.write("\n")
# file.close()
print("All Done .\n")
