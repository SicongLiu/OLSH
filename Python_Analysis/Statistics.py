'''
Created on Feb 24, 2018

@author: sicongliu
'''

import numpy as np
import math
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt


def computer_qhull_statistics(data_file_path, k):

    num_of_data_elements_cum_sum = 0

    cum_sum = []
    data_elements = []
    for i in range(k):
        # print 'Qhull Layer: ', str(i)
        data_file = data_file_path + str(i)
        f = open(data_file, 'r')
        lines = f.readlines()
        first_line = lines[0]
        metadata = first_line.split(" ")
        second_line = lines[1]
        num_of_data_elements = float(second_line.split('\n')[0])
        num_of_data_elements = int(num_of_data_elements)
        num_of_dimensions = float(metadata[0])
        num_of_dimensions = int(num_of_dimensions)

        data_elements.append(num_of_data_elements)
        num_of_data_elements_cum_sum += num_of_data_elements
        cum_sum.append(num_of_data_elements_cum_sum)

    distribution = []
    # number of layers for data element retrieval
    for i in range(k):
        # num of layers
        cur_data_elements = data_elements[i]
        cur_distribution = 0
        for j in range(k):
            weight = 1/(math.log(j+1)+1)
            cur_sum = cum_sum[j]
            cur_distribution += weight * cur_data_elements / cur_sum
        distribution.append(cur_distribution)
    return distribution


def plot_histogram(distribution, save_data_folder, my_aff_name):
    print ('Distribution to be printed: ', distribution)
    fig = plt.figure()
    # plt.hist(distribution)
    # plt.plot(distribution)
    x_axis_value = np.arange(1,len(distribution)+1, 1)
    plt.plot(x_axis_value, distribution)
    # plt.xticks(distribution)
    plt.title("Distribution Histogram")
    plt.xlabel("Layer Index (Integer)")
    plt.ylabel("Pi_Value")
    fig_name = save_data_folder + '.png'
    fig.savefig(fig_name)


if __name__ == '__main__':
    # root_folder = '/Users/sliu104/Desktop/StreamingTopK/qhull/bin/data_sample'
    # my_aff_name = 'data_ICDE_2010'
    # data_file_path = root_folder + '/' + my_aff_name + '_qhull_layer_'
    #
    # # number of interesting layers
    # k = 2
    # my_distribution = computer_qhull_statistics(data_file_path, k)
    #
    # # my_save_data_folder = './'
    # my_save_data_folder = data_file_path
    # plot_histogram(my_distribution, my_save_data_folder, my_aff_name)

    file_count = 5
    # k = 10
    k = 4
    # k = 3
    # k = 2
    # k = 1

    root_folder = '/Users/sliu104/Desktop/StreamingTopK/qhull/DATA/Data_With_Boundaries/2D_data'
    MY_AFF_NAME = '2d_test'

    # root_folder = '/Users/sliu104/Desktop/StreamingTopK/qhull/DATA/4D_data'
    # MY_AFF_NAME = '4d_test'

    # root_folder = '/Users/sliu104/Desktop/StreamingTopK/qhull/DATA/6D_data'
    # MY_AFF_NAME = '6d_test'

    # root_folder = '/Users/sliu104/Desktop/StreamingTopK/qhull/DATA/8D_data'
    # MY_AFF_NAME = '8d_test'

    MY_SAVE_DATA_FOLDER = root_folder
    for i in range(2, file_count + 1):
        data_file_path = root_folder + '/' + MY_AFF_NAME + str(i) + '_qhull_layer_'
        my_distribution = computer_qhull_statistics(data_file_path, k)
        # print 'Currenty Distribution: ',my_distribution
        my_save_data_folder = MY_SAVE_DATA_FOLDER + str(i)
        plot_histogram(my_distribution, my_save_data_folder, MY_AFF_NAME)

    print ('Qhull Statistics Done')

