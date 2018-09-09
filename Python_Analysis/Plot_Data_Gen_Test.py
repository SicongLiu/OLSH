import matplotlib.pyplot as plt
import numpy as np

random_file = "random_2_1000.txt"
correlated_file = "correlated_2_1000.txt"
anti_correlated_file = "anti_correlated_2_1000.txt"

data = np.loadtxt(anti_correlated_file)
plt.plot(data[:, 0], data[:, 1], 'o')
# fig = plt.figure()
# ax = plt.subplot(111)
# ax.plot(data[:, 0], data[:, 1])
# plt.title('Legend inside')
# ax.legend()
plt.show()
