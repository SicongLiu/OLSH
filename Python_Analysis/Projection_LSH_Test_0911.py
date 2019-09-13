import os
import re
import sys
import numpy as np
import math
# import pandas as pd
# import matplotlib.pyplot as plt
from collections import Counter


def dot(K, L):
    if len(K) != len(L):
        return 0
    return float("{0:.5f}".format(sum(i[0] * i[1] for i in zip(K, L))))


def angle(data_, norm_data_, query_, norm_query_):
    return math.acos(1.0 * dot(data_, query_) / (norm_data_ * norm_query_))


def compute_recall(grountTruth_, ret_index_):
    intersection = len(list(set(grountTruth_).intersection(set(ret_index_))))
    return float(1.0 * intersection / len(grountTruth_))


def transform_query(query_, query_norm_, pivot_, pivot_norm_):
    alpha_ = angle(query_, query_norm_, pivot_, pivot_norm_)
    tuple_ = []
    t1_ = (math.sin(alpha_) * math.sin(alpha_) - 1)/(2 * math.cos(alpha_))
    t2_ = math.cos(alpha_)
    tuple_.append(t1_)
    tuple_.append(t2_)
    return tuple_


def transform_data(data_, data_norm_, pivot_, pivot_norm_):
    beta_ = angle(data_, data_norm_, pivot_, pivot_norm_)
    tuple_ =[]
    t1_ = (-1.0) * data_norm_ * math.cos(beta_)
    t2_ = (-1.0) * data_norm_ * (math.sin(beta_) * math.sin(beta_) - 1) / (2 * math.cos(beta_))
    # t1_ = data_norm_ * math.cos(beta_)
    # t2_ = data_norm_ * (math.sin(beta_) * math.sin(beta_) - 1) / (2 * math.cos(beta_))
    tuple_.append(t1_)
    tuple_.append(t2_)
    return tuple_



dimension = 100
cardinality = 1000
data_type = 'random_'
data_file = data_type + str(dimension) + '_' + str(cardinality) + '.txt'
query_file = 'query_' + str(dimension) + 'D' + '.txt'

# load data
f = open(data_file, 'r')
lines = f.readlines()
cur_dim = int(lines[0])
cur_card = int(lines[1])
data_list = []
data_norm_list = []
for i in range(cur_card):
    current_data_record = np.fromstring(lines[i + 2], dtype=float, sep=' ')
    current_data_record = np.asarray(current_data_record)
    data_list.append(current_data_record)
    temp_norm = np.linalg.norm(current_data_record)
    # data_norm_list.append(format(temp_norm, '.5f'))
    data_norm_list.append(float("{0:.5f}".format(temp_norm)))
f.close()

# load query
f = open(query_file, 'r')
lines = f.readlines()

cur_dim = int(lines[0])
cur_card = int(lines[1])
query_list = []
query_norm_list = []
for i in range(cur_card):
    current_data_record = np.fromstring(lines[i + 2], dtype=float, sep=' ')
    current_data_record = np.asarray(current_data_record)
    # compute ground truth
    query_list.append(current_data_record)
    temp_norm = np.linalg.norm(current_data_record)
    # data_norm_list.append(format(temp_norm, '.5f'))
    query_norm_list.append(float("{0:.5f}".format(temp_norm)))
f.close()

# compute and rank results based on theta_min = beta - alpha
top_k = 50
pivot = np.zeros(dimension)
pivot[77] = 1
pivot_norm = 1

recall_list = []
recall_list_transform = []
for ii in range(query_list.__len__()):  # for each query we have top_k results
    theta_list = []
    alpha = angle(query_list[ii], query_norm_list[ii], pivot, pivot_norm)

    tuple_query = transform_query(query_list[ii], query_norm_list[ii], pivot, pivot_norm)
    dot_val_list = []
    dot_val_transform_list = []
    for jj in range(data_list.__len__()):

        beta = angle(data_list[jj], data_norm_list[jj], pivot, pivot_norm)
        tuple_data = transform_data(data_list[jj], data_norm_list[jj], pivot, pivot_norm)

        dot_val_transform_list.append(dot(tuple_query, tuple_data))
        # use Jaccard set similarity as ground truth
        theta = abs(beta - alpha)
        theta_list.append(theta)
        dot_val_list.append(dot(query_list[ii], data_list[jj]))  # dot product value, the larger the better

    grountTruth = np.argsort(dot_val_list)[::-1]
    grountTruth = grountTruth[0:top_k]

    transform_list_ground_truth = np.argsort(dot_val_transform_list)[::-1]
    transform_list_ground_truth = transform_list_ground_truth[0:top_k]

    ret_index = np.argsort(theta_list)  # rank angle-distance theta, ascending order -- the smaller the better
    ret_index = ret_index[0:top_k]
    recall_val = compute_recall(grountTruth, ret_index)
    recall_list.append(recall_val)
    recall_list_transform.append(compute_recall(grountTruth, transform_list_ground_truth))

print(1.0 * sum(recall_list)/recall_list.__len__())
print(1.0 * sum(recall_list_transform)/recall_list_transform.__len__())

print('Done')
