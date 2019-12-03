import matplotlib
import matplotlib.pyplot as plt
import numpy as np


data_folder = '/Users/sicongliu/Desktop/StreamingTopK/'
data_type = 'anti_correlated'
cardinality = 1000
dimension = 2
file_name = data_folder + data_type + '_' + str(dimension) + '_' + str(cardinality) + '.txt'
f = open(file_name, 'r')
lines = f.readlines()

cur_dim = int(lines[0])
cur_card = int(lines[1])
data_list = []
for kk in range(cur_card):
    current_data_record = np.fromstring(lines[kk + 2], dtype=float, sep=' ')
    current_data_record = np.asarray(current_data_record)
    data_list.append(current_data_record)

f.close()
data_list = np.asarray(data_list)
x_data = data_list[:, 0]
y_data = data_list[:, 1]

# _ = plt.scatter(data_list)
_ = plt.scatter(x_data, y_data, c='r', label='data')
print('done')