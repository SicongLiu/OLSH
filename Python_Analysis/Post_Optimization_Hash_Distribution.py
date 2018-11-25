import math
import numpy as np

top_m = 25
top_m_cardinality = 275400
hash_budget = top_m_cardinality * 2
hash_used = 534961

data_list = [1519, 2902, 4201, 5435, 6366, 7395, 8147, 8984, 9622, 10307, 11053, 11551, 11982, 12620, 13014, 13552,
             13894, 14338, 14754, 14810, 15288, 15585, 15876, 16060, 16145]
KList_Log = [11, 12, 13, 13, 13, 13, 13, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14]
LList = [26, 14, 10, 7, 6, 5, 4, 3, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
weight = [0.081600306, 0.079476028, 0.077041773, 0.074457424, 0.069096951, 0.065782109, 0.060756796, 0.057006843,
          0.052492599, 0.048674672, 0.04538301, 0.041342773, 0.037406774, 0.034323352, 0.030750563, 0.027688552,
          0.024378937, 0.021398294, 0.018482749, 0.015291434, 0.012672056, 0.009973976, 0.0073666, 0.004810476,
          0.002344953]

collision_probility = 0.9
smallest = min(data_list)
smallest_index = data_list.index(min(data_list))

total_error = 0.412502654
total_error_gain = 0
flag = False
while hash_used + smallest < hash_budget:
    print("still got hash space left")
    # the condition of improvement is to check if the total error rate drops

    # loop through, keep track of hash-relocation and error rate drop
    # find the biggest error gain, while keep hash-resources constraints
    # update hash_used, LList
    delta_error_list = []
    for i in range(len(data_list)):
        cur_k = KList_Log[i]
        cur_l = LList[i]
        c_old = math.pow((1 - math.pow(collision_probility, cur_k)), cur_l)

        # each time increment hash layer by 1
        c_new = math.pow((1 - math.pow(collision_probility, cur_k)), (cur_l+1))
        delta_error_list.append((c_old - c_new))

    # sort and check each delta_error
    delta_error_list = np.asarray(delta_error_list)
    sorted_index = delta_error_list.argsort()[::-1][:len(delta_error_list)]
    sorted_pivot = 0
    while sorted_pivot < len(sorted_index):
        cur_index = sorted_index[sorted_pivot]

        # each time increment hash layer by 1
        # temp_hash_used = hash_used + (LList[cur_index] + 1) * data_list[cur_index]
        temp_hash_used = hash_used + data_list[cur_index]
        if temp_hash_used < hash_budget:
            LList[cur_index] = LList[cur_index] + 1
            hash_used = hash_used + data_list[cur_index]
            print("Update index: " + str(cur_index + 1))
            break
        sorted_pivot = sorted_pivot + 1

# re-compute total error
print(LList)

total_error = 0
for i in range(len(LList)):
    cur_k = KList_Log[i]
    cur_l = LList[i]
    total_error = total_error + weight[i] * math.pow((1 - math.pow(collision_probility, cur_k)), cur_l)
print("Updated total error: " + str(total_error))
print("all used, done")



