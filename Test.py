'''
Created on Feb 20, 2018

@author: sicongliu
'''

import numpy as np

data_file_path = '/Users/sliu104/Desktop/StreamingTopK/qhull/bin/data_sample/data_ICDE_2010'
f = open(data_file_path, 'r')
lines = f.readlines()


# lines = np.loadtxt(data_file_path, skiprows=1)


print len(lines)
print lines[0]
print lines[1]
array = []
print '-------------------'
for i in range(3, len(lines)):
    cur_line = lines[i]
    my_line = np.fromstring(cur_line, dtype=float, sep=' ')

    print 'my line: ', my_line

    # cur_line = cur_line.replace('\n', '')
    # cur_line = cur_line.replace(' ', ',')
    # array.append(np.asarray(cur_line))
    # array.append(cur_line)
    # cur_array = np.asarray(cur_line)
    # print cur_array
    array.append(my_line)
print '-------------------'
print array[0]

print array
temp = (0.1, 0.3)
target = np.asarray(temp)


print 'target array: ', target

print '-----search target array: '
for i in range(len(array)):
    if np.array_equal(target, array[i]):
        print i

print '-----Dumy test: '
print np.array_equal([1, 2], [1, 2])
print np.array_equal(array[0], target)