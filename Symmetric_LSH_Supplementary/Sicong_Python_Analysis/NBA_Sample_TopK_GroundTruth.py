import numpy as np
from scipy.spatial import distance


def compute_top_k(input_data, query, topk):
    euclidean_dist = []
    for i in range(0, input_data.shape[0]):
        # using Euclidean distance
        cur_distance = distance.euclidean(input_data[i, :], query)
        euclidean_dist.append(cur_distance)
    euclidean_dist = np.array(euclidean_dist)
    # range from [0, topk-1]
    top_k_index = np.argsort(euclidean_dist)[0: topk]
    return top_k_index, input_data[top_k_index, :], euclidean_dist[top_k_index]


def compute_top_k_weight(input_data, query, topk):
    input_data = np.array(input_data)
    query = np.array(query)
    # use dot product
    dot_product = np.multiply(input_data, query)
    dot_product = np.array(dot_product)
    temp_sum = np.sum(dot_product, axis=1)
    # range from [size - topk, size - 1]
    top_k_index = np.argsort(temp_sum)[temp_sum.shape[0] - topk: temp_sum.shape[0]]
    return top_k_index, input_data[top_k_index, :], temp_sum[top_k_index]


if __name__ == '__main__':
    # topk of interest
    k = 50
    data_file_name = 'NBA_data_for_matlab'
    data = np.loadtxt(data_file_name, delimiter=' ')
    data_size = data.shape[0]
    data_dimension = data.shape[1]

    query_1 = 'NBA_query_1_for_matlab'
    query_2 = 'NBA_query_2_for_matlab'
    query_3 = 'NBA_query_3_for_matlab'

    q_1 = np.loadtxt(query_1)
    q_2 = np.loadtxt(query_2)
    q_3 = np.loadtxt(query_3)

    index_1, topk_data_1, topk_value_1 = compute_top_k(data, q_1, k)
    index_2, topk_data_2, topk_value_2 = compute_top_k(data, q_2, k)
    index_3, topk_data_3, topk_value_3 = compute_top_k(data, q_3, k)

    # save result
    save_query_1 = 'result_1.csv'
    save_query_2 = 'result_2.csv'
    save_query_3 = 'result_3.csv'

    # inplace concatenate and save
    np.savetxt(save_query_1, np.column_stack((index_1, topk_data_1, topk_value_1)), delimiter=',')
    np.savetxt(save_query_2, np.column_stack((index_2, topk_data_2, topk_value_2)), delimiter=',')
    np.savetxt(save_query_3, np.column_stack((index_3, topk_data_3, topk_value_3)), delimiter=',')

    w_index_1, w_topk_data_1, w_topk_value_1 = compute_top_k_weight(data, q_1, k)
    w_index_2, w_topk_data_2, w_topk_value_2 = compute_top_k_weight(data, q_2, k)
    w_index_3, w_topk_data_3, w_topk_value_3 = compute_top_k_weight(data, q_3, k)\

    # save result with weight option
    save_query_w_1 = 'result_w_1.csv'
    save_query_w_2 = 'result_w_2.csv'
    save_query_w_3 = 'result_w_3.csv'

    np.savetxt(save_query_w_1, np.column_stack((w_index_1, w_topk_data_1, w_topk_value_1)), delimiter=',')
    np.savetxt(save_query_w_2, np.column_stack((w_index_2, w_topk_data_2, w_topk_value_2)), delimiter=',')
    np.savetxt(save_query_w_3, np.column_stack((w_index_3, w_topk_data_3, w_topk_value_3)), delimiter=',')

    print('All Done.\n')

