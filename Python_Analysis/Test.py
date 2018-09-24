'''
Created on Feb 20, 2018

@author: sicongliu
'''

import numpy as np

count = [1, 2, 3, 4]
ll = ['a', 'b', 'c', 'd']

output = "List" + str(count) + ""

print ','.join(ll)

mylist = []
list1 = [1, 2, 3]
list2 = [2, 3, 4]
mylist.append(list1)

mylist.append(list2)

print(mylist)
print(len(mylist))