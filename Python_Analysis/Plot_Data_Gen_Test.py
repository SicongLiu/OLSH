import matplotlib.pyplot as plt
import numpy as np

random_file = "random_data.txt"
correlated_file = "correlated_data.txt"
anti_correlated_file = "anticorrelated_data.txt"

data = np.loadtxt(correlated_file)
plt.plot(data[:, 0], data[:, 1], 'o')
# fig = plt.figure()
# ax = plt.subplot(111)
# ax.plot(data[:, 0], data[:, 1])
# plt.title('Legend inside')
# ax.legend()
plt.show()
