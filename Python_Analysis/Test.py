import numpy as np
# x = np.array([3, 4])
# y = np.linalg.norm(x)
#
# yy = np.std(x)

# import matplotlib.pyplot as plt
import math
from  collections import Counter

list1 = []
list2 = [1, 2, 3, 4]
list3 = [2, 3, 4, 5]
list1.extend(list2)
list1.extend(list3)

list1 = set(list1)
print(list1)
print(list1.__len__())