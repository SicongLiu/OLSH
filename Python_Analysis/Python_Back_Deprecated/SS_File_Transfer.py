from openpyxl import load_workbook
import random
import pandas as pd
import numpy as np
from numpy import genfromtxt

def column_row_index(column_name, row_id):
    return column_name + str(row_id)


# sl0 sl1 slLabel movieId id slAttr movieName
sl0_column = 'A'
sl1_column = 'B'
slLabel_column = 'C'
movieId_column = 'D'
id_column = 'E'
slAttr_column = 'F'
movieName_column = 'G'

text_folder = "/Users/sicongliu/Desktop/TODS_Test_Data_Strata/"
csv_folder = "/Users/sicongliu/Desktop/TODS_Test_Data_Strata/"

# input_text_file = text_folder + 'anti_correlated_2_324.txt'
# csv_file = csv_folder + 'test_data_anti.csv'

# input_text_file = text_folder + 'correlated_2_118.txt'
# csv_file = csv_folder + 'test_data_corr.csv'

# input_text_file = text_folder + 'anti_correlated_2_200000_qhull_layer_6'
# csv_file = csv_folder + 'test_data_anti_6.csv'

input_text_file = text_folder + 'correlated_2_200000_qhull_layer_5'
csv_file = csv_folder + 'test_data_corr_5.csv'

slLabel_ = ""
movieName_ = ""
f1 = open(input_text_file, 'r')
lines = f1.readlines()
dimension = int(lines[0])
cardinality = int(lines[1])

data_frame = pd.read_csv(csv_file)
print(data_frame.columns.values)
for i in range(2, lines.__len__()):
    print("line:", i)
    data = np.fromstring(lines[i], dtype=float, sep=' ')

    data1 = round(float(data[0]) * 10000)
    data2 = round(float(data[1]) * 10000)
    slAttr = random.randint(1, 101)
    movieID = i - 1
    id = i - 1
    column_row_index_sl0 = column_row_index(sl0_column, id)
    column_row_index_sl1 = column_row_index(sl1_column, id)
    column_row_index_slLabel = column_row_index(slLabel_column, id)
    column_row_index_movieId = column_row_index(movieId_column, id)
    column_row_index_id = column_row_index(id_column, id)
    column_row_index_slAttr = column_row_index(slAttr_column, id)
    column_row_index_movieName = column_row_index(movieName_column, id)

    data_frame.at[id-1, 'sl0'] = data1
    data_frame.at[id-1, 'sl1'] = data2
    data_frame.loc[id - 1, 'slLabel'] = slLabel_
    data_frame.at[id-1, 'movieId'] = movieID
    data_frame.at[id-1, 'id'] = id
    data_frame.loc[id-1, 'slAttr'] = slAttr
    data_frame.loc[id-1, 'movieName'] = movieName_

# print(data_frame)
data_frame.to_csv(csv_file, index=False)
f1.close()
print('Done')
