'''
Created on Feb 20, 2018

@author: sicongliu
'''

import numpy as np

arr = np.asarray([[1, 2, 3, 4, 5], [6, 7, 8, 9, 5], [2, 3, 4, 5, 6], [6, 7, 8, 9, 9]])

arr1 = np.asarray([1, 2, 3, 4, 5])
arr2 = np.asarray([6, 7, 8, 9, 0])
print(arr)
print(arr1[0])
print(arr1[4])

print(arr1.shape)
rows, columns = np.where((arr == arr1))
rr = np.where((arr == arr1).all(axis=1))[0]
arr = np.delete(arr, rows[0], 0)

print("rows: " + str(rows))

print("columns: " + str(columns))

rows, columns = np.where(arr == arr2)
arr = np.delete(arr, rows[0], 0)

print(arr)
print("shape: " + str(arr.shape))

print("rows: " + str(rows))

print("columns: " + str(columns))