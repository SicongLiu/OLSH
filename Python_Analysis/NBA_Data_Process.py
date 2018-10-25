#!/usr/bin/env python
from __future__ import print_function
import os
import numpy as np
import pandas as pd
import xlwt
import xlrd

# excel_path = '../NBA_Data/Oct_24_no_partial'

excel_directory = '../NBA_Data/Oct_24_with_partial/'
files = os.listdir(excel_directory)
files_xls = [f for f in files if f[-4:] == 'xlsx']

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
            cur_record.append(value)
        total_data.append(cur_record)
        total_record_count = total_record_count + 1

print("total number of record: " + str(total_record_count))
file = open("NBA_Data.txt", "w")
file.write(str(dimension))
file.write("\n")
file.write(str(total_record_count))
file.write("\n")
# write file in text file
for i in range(total_record_count):
    s = "  ".join(map(str, total_data[i]))
    file.write(s)
    file.write("\n")
file.close()
print("All Done .\n")
