'''
Created on Feb 20, 2018

@author: sicongliu
'''

import numpy as np
import math
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

data_file_path = '/Users/sliu104/Desktop/StreamingTopK/qhull/bin/data_sample/data_ICDE_2010'
f = open(data_file_path, 'r')
lines = f.readlines()


t = 10
print(t%10)
# lines = np.loadtxt(data_file_path, skiprows=1)

a = [0] * 10
print(a.__len__())
for i in range(0, 10):
    print(i)
array = [0, 1, 2, 3, 4, 5]
print(np.mean(array))

print len(lines)
print lines[0]
ss = lines[0]
sst = ss.split(" ")
print sst[2]
print sst[0]
num_of_data_elements = sst[2]



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
print np.array_equal(array, target)
rows, columns = np.where(array == target)
print 'research result: ', rows
print 'result len: ', len(rows)
print rows
print columns

# print array[result[0]]
print '-----------------'

# print array[result[0][0]]
print 'before deletion: ', array


print '-----------------'

array.pop(rows[0])
# np.delete(array, rows)
# array.remove(result[0][0], result[0][1])
# array.remove(result[1][0], result[1][1])
print 'after deletion: ', array

print '----- log function ------------'
print math.log(math.e)

print '----- plot histogram ------------'
my_array = [1.3691350682185257, 0.8214810409311155]

xx = np.arange(1,len(my_array)+1, 1)
print xx
print 'Array to be ploted: ', my_array

fig = plt.figure()
# plt.plot(my_array)
plt.ylim([0, 2])
plt.plot(xx, my_array)

plt.title("Gaussian Histogram")

plt.xlabel("Pi_Value")
plt.ylabel("Percentage")

# fig_name = 'test_plot.png'
# fig = plt.gcf()

plt.show()
# plt.savefig('books_read.png')
# fig.savefig('books_read.png')

# plot_url = py.plot_mpl(fig, filename='mpl-basic-histogram')


