import math
import numpy as np


def compute_collision_prob(dimension_, data_list_):
    prob_list_ = []
    for ii in data_list_:
        theta = pow((2 * math.pi/ii), (1/(dimension_ - 1)))
        collision = 1 - theta / math.pi
        prob_list_.append(collision)
    return prob_list_


def compute_error_rate(prob_list_, K_List_, L_List_, weight_list_):
    total_error = 0
    for i in range(len(L_List_)):
        cur_k = K_List_[i]
        cur_l = L_List_[i]
        total_error = total_error + weight_list_[i] * math.pow((1 - math.pow(prob_list_[i], cur_k)), cur_l)
    return total_error


def compute_weights(data_list_, top_m):
    data_list_ = np.asarray(data_list_)
    contribution_list = []
    weight_list_ = []
    data_list_cumsum = np.cumsum(data_list_)
    for i in range(top_m):
        c_h = data_list_[i]
        temp_contribution = 0
        for j in range(i, top_m):
            denominator = data_list_cumsum[j]
            temp_contribution = 1.0 * temp_contribution + (1.0 * c_h/denominator)
        contribution_list.append(temp_contribution)
    sum_contribution = sum(contribution_list)
    for i in range(top_m):
        temp_weight = (1.0 * contribution_list[i])/sum_contribution
        weight_list_.append(temp_weight)
    return weight_list_


def total_replication(K_List_, L_List, data_list_):
    ret = 0
    for ii in range(data_list_.__len__()):
        ret = ret + L_List[ii] * data_list_[ii]
    return ret




# same # of onion layers, K and L values
# different dims, data_cardinality
layer_count = 14
dim_1 = 4
dim_2 = 7

# weight_list_1 = np.ones(layer_count)
# weight_list_2 = np.ones(layer_count)

K_List_1 = [10, 11, 11, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12]
K_List_2 = [14, 15, 15, 15, 15, 15, 15, 14, 13, 13, 12, 11, 9, 6]

L_List_1 = [27, 18, 13, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
L_List_2 = [14, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3]

data_list_1 = [792, 1307, 1791, 2072, 2323, 2586, 2679, 2731, 2833, 2906, 2945, 3024, 2987, 3002]
data_list_2 = [15077, 27635, 32154, 30809, 27020, 22086, 16768, 11943, 7787, 4794, 2517, 1032, 331, 47]

weight_list_1 = compute_weights(data_list_1, layer_count)
weight_list_2 = compute_weights(data_list_2, layer_count)

prob_list_1 = compute_collision_prob(dim_1, data_list_1)
prob_list_2 = compute_collision_prob(dim_2, data_list_2)

error_1 = compute_error_rate(prob_list_1, K_List_1, L_List_1, weight_list_1)
error_2 = compute_error_rate(prob_list_2, K_List_2, L_List_2, weight_list_2)

data_rep_1 = total_replication(K_List_1, L_List_1, data_list_1)
data_rep_2 = total_replication(K_List_2, L_List_2, data_list_2)

print(error_1)
print(error_2)

print(data_rep_1)
print(data_rep_2)
