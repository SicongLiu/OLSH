import numpy as np
import os

a = ((1, 2, 3), (2, 1, 3), (2, 3, 4), (5, 6, 7))
a = np.asarray(a)

# # total_index = (0:3)
# total_index= range(4)
# total_index = set(total_index)
# # total_index.add(1)
# # total_index.add(2)
# # total_index.add(3)
#
# index = {0}
# index.add(0)
# index.add(1)
# remain_index = index


# print(total_index.difference(index))
#
# print(index.difference(total_index))
dim = 3
card = 4
command_bin_folder = '/Users/sicongliu/Desktop/StreamingTopK'
# command_line = command_bin_folder + '/main ' + a + ' ' + str(dim) + ' ' + str(card)
# output = os.popen(command_line).read()
# print(output)

result = np.arange(20, dtype=np.float).reshape((2, 10))

print(type(result))
print(type(a))
