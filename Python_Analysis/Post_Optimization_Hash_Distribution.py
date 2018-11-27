import math
import numpy as np

# values below all read from excel sheet
####################################################################################

# for optimized approach
anti_weight_list = []
corr_weight_list = []
random_weight_list = []

top_m = 25
top_m_cardinality = 275400
hash_budget = top_m_cardinality * 2
hash_used = 534961

data_list = [1519, 2902, 4201, 5435, 6366, 7395, 8147, 8984, 9622, 10307, 11053, 11551, 11982, 12620, 13014, 13552,
             13894, 14338, 14754, 14810, 15288, 15585, 15876, 16060, 16145]


def compute_weights(data_list_):
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


weight_list = compute_weights(data_list)
KList_Log = [11, 12, 13, 13, 13, 13, 13, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14]
L_Opt_List = [26, 14, 10, 7, 6, 5, 4, 3, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
L_Uni_List = [15, 8, 5, 4, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1]
# weight = [0.081600306, 0.079476028, 0.077041773, 0.074457424, 0.069096951, 0.065782109, 0.060756796, 0.057006843,
#           0.052492599, 0.048674672, 0.04538301, 0.041342773, 0.037406774, 0.034323352, 0.030750563, 0.027688552,
#           0.024378937, 0.021398294, 0.018482749, 0.015291434, 0.012672056, 0.009973976, 0.0073666, 0.004810476,
#           0.002344953]

####################################################################################
collision_probility = 0.9
smallest = min(data_list)
smallest_index = data_list.index(min(data_list))

total_error = 0.412502654
total_error_gain = 0
flag = False
while hash_used + smallest <= hash_budget:
    print("still got hash space left")
    # the condition of improvement is to check if the total error rate drops

    # loop through, keep track of hash-relocation and error rate drop
    # find the biggest error gain, while keep hash-resources constraints
    # update hash_used, LList
    delta_error_list = []
    for i in range(len(data_list)):
        cur_k = KList_Log[i]
        cur_l = L_Opt_List[i]
        c_old = math.pow((1 - math.pow(collision_probility, cur_k)), cur_l)

        # each time increment hash layer by 1
        c_new = math.pow((1 - math.pow(collision_probility, cur_k)), (cur_l+1))
        delta_error_list.append((c_old - c_new))

    # sort and check each delta_error
    delta_error_list = np.asarray(delta_error_list)
    # sort in descending order
    sorted_index = delta_error_list.argsort()[::-1][:len(delta_error_list)]
    sorted_pivot = 0
    while sorted_pivot < len(sorted_index):
        cur_index = sorted_index[sorted_pivot]

        # each time increment hash layer by 1
        # temp_hash_used = hash_used + (LList[cur_index] + 1) * data_list[cur_index]
        temp_hash_used = hash_used + data_list[cur_index]
        if temp_hash_used < hash_budget:
            L_Opt_List[cur_index] = L_Opt_List[cur_index] + 1
            hash_used = hash_used + data_list[cur_index]
            print("Update index: " + str(cur_index + 1))
            break
        sorted_pivot = sorted_pivot + 1

# re-compute total error
print(L_Opt_List)

# To-DO:
# save it back to excel file

total_error = 0
total_hash_used = 0
for i in range(len(L_Opt_List)):
    cur_k = KList_Log[i]
    cur_l = L_Opt_List[i]
    total_error = total_error + weight_list[i] * math.pow((1 - math.pow(collision_probility, cur_k)), cur_l)
    total_hash_used = total_hash_used + data_list[i] * cur_l
print("Updated total error: " + str(total_error))
print("total hash used: " + str(total_hash_used))
print("Optimized approach done")

####################################################################################
# for uniformly distributed approach
# uniformly pick one that fits the current hash budget instead of the one minimizing total error rate

import random

flag = False
hash_used = 524822
data_list = np.asarray(data_list)
while hash_used + smallest <= hash_budget:
    print("still got hash space left")
    # sort in descending order

    sorted_index = data_list.argsort()[::-1][:len(data_list)]

    temp_pivot_list = []
    # first find all the allow current hash re-allocation
    for i in range(len(sorted_index)):
        temp_pivot_index = sorted_index[i]
        if hash_used + data_list[temp_pivot_index] <= hash_budget:
            temp_pivot_list.append(temp_pivot_index)
    # randomly pick one from those
    cur_pivot = random.choice(temp_pivot_list)
    # update L_Uni_List, hash_used
    L_Uni_List[cur_pivot] = L_Uni_List[cur_pivot] + 1
    hash_used = hash_used + data_list[cur_pivot]

total_error = 0
total_hash_used = 0
for i in range(len(L_Uni_List)):
    cur_k = KList_Log[i]
    cur_l = L_Uni_List[i]
    total_error = total_error + weight_list[i] * math.pow((1 - math.pow(collision_probility, cur_k)), cur_l)
    total_hash_used = total_hash_used + data_list[i] * cur_l
print(L_Uni_List)
print("Updated total error: " + str(total_error))
print("total hash used: " + str(total_hash_used))
print("Uniform approach done")