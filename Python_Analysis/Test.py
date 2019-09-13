import numpy as np
# x = np.array([3, 4])
# y = np.linalg.norm(x)
#
# yy = np.std(x)

# import matplotlib.pyplot as plt
import math
from  collections import Counter


def dot(K, L):
    if len(K) != len(L):
        return 0
    return sum(i[0] * i[1] for i in zip(K, L))


def angle(data_, norm_data_, query_, norm_query_):
    return math.acos(dot(data_, query_) / (norm_data_ * norm_query_))


# print(math.acos(0.950794 / (1 * 0.95079)))
print(0.950794 / (1 * 0.95079))

3 * (-1)