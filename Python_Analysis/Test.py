'''
Created on Feb 20, 2018

@author: sicongliu
'''

import numpy as np
import math
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from operator import itemgetter

a = [1, 4, 5, 6]
b = [8, 1, 2, 3]
c = [1, 4, 5, 6]
d = [1, 2, 3, 4]
# tt = [np.asarray(a), np.array(b), np.array(c)]
tt = [a, b, c]
print (tt.index([1, 4, 5, 6]))
print(a in tt)
print(d in tt)

print(np.isin(tt, a))
print(type(tt))
# tt = np.asarray(tt)
aa = [1, 4, 5, 6]
aa = np.asarray(aa)
index = np.where(tt == aa)
print (index)