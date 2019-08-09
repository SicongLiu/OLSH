import csv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


# csv_file = 'Apple_Stock_Data.csv'
# data_frame = pd.read_csv(csv_file)
# print(data_frame['Stock Prices'])
# plt.figure()
#
# data_frame.plot()
# plt.ylabel('Price [USD]')
# cur_axes = plt.gca()
# cur_axes.axes.get_xaxis().set_ticks([])
# print("Done")


# csv_file = 'co_emissions_us.csv'
# data_frame = pd.read_csv(csv_file)
# print(data_frame['Emissions'])
# plt.figure()
#
# data_frame.plot()
# # plt.xlabel('Year') # 1900 -- 2015
# plt.ylabel('Billion Tonnes Per Year')
#
# cur_axes = plt.gca()
# cur_axes.axes.get_xaxis().set_ticks([])
# # cur_axes.axes.get_yaxis().set_ticks([])
# print("Done")



# buckets = [0] * 527
#
# loc1 = [50, 55]
# loc2 = [205, 210]
# loc3 = [310, 315]
# loc4 = [410, 415]
#
# noise1 = np.random.normal(0,0.1,5)
# noise2 = np.random.normal(0,0.1,5)
# noise3 = np.random.normal(0,0.1,5)
# noise4 = np.random.normal(0,0.1,5)
#
# noise5 = np.random.normal(0,0.1,527)
# buckets[loc1[0]: loc1[1]] = noise1
# print(len(buckets))
# buckets[loc2[0]: loc2[1]] = noise2
# print(len(buckets))
# buckets[loc3[0]: loc3[1]] = noise3
# print(len(buckets))
# buckets[loc4[0]: loc4[1]] = noise4
# print(len(buckets))
# print(buckets.__len__())
#
#
#
# csv_file = '7-8.csv'
# data_frame = pd.read_csv(csv_file)
# # print(data_frame['Emissions'])
# plt.figure()
#
# print(data_frame['a'].size)
# data_frame['a'] = data_frame['a'] + buckets
# data_frame['a'] = data_frame['a'] + noise5
# # data_frame['a'].plot()
# data_frame.plot()
# # plt.ylabel('Billion Tonnes Per Year')
#
# plt.axis('off')
# cur_axes = plt.gca()
# cur_axes.get_legend().remove()
# cur_axes.axes.get_xaxis().set_ticks([])
# # cur_axes.axes.get_yaxis().set_ticks([])
# print("Done")




csv_file = '7-12.csv'
data_frame = pd.read_csv(csv_file)
# print(data_frame['Emissions'])
plt.figure()

# data_frame['a'].plot()
data_frame.plot()
# plt.ylabel('Billion Tonnes Per Year')

plt.axis('off')
cur_axes = plt.gca()
cur_axes.get_legend().remove()
cur_axes.axes.get_xaxis().set_ticks([])
# cur_axes.axes.get_yaxis().set_ticks([])
print("Done")