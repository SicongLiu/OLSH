'''
Created on Feb 20, 2018

@author: sicongliu
'''

a = [1, 2, 3, 4]
a.append(5)
b = [1, 2, 3, 4]

c = []
c.append(a)
c.append(b)

d = []
print(d.__len__())
d.append(5)
d.append(d[d.__len__() - 1] + 5)
d.append(5)
d.append(5)
d.append(5)

print(d)