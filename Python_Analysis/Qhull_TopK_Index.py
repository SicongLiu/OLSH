import numpy as np
from operator import itemgetter
import os

# search the index of the TopK, output to file with layer index
def serachTopK(file_path, top_k_data, top_k_index, top_k_sim, layer_index):
    layer_file = open(file_path, 'r')
    data_lines = layer_file.readlines()
    data = []
    for ii in range(2, len(data_lines)):
        cur_line = data_lines[ii]
        my_line = np.fromstring(cur_line, dtype=float, sep=' ')
        my_line = my_line.tolist()
        data.append(my_line)
    layer_file.close()

    result_struct = []
    for ii in range(len(top_k_index)):
        cur_top_k_data = top_k_data[ii]
        cur_top_k_data = cur_top_k_data.tolist()
        # look up cur_data in data
        if cur_top_k_data in data:
            cur_top_k_data.append(top_k_sim[ii])
            cur_top_k_data.append(top_k_index[ii])
            cur_top_k_data.append(layer_index)
            result_struct.append(cur_top_k_data)
    return result_struct


# compute TopK Ground Truth across all data, output similarity, index and data coordinates
def computeTopK_All_Data(file_path, dim, size, query_path):
    f1 = open(file_path, 'r')
    data_lines = f1.readlines()
    data = []
    for ii in range(2, len(data_lines)):
        cur_line = data_lines[ii]
        my_line = np.fromstring(cur_line, dtype=float, sep=' ')
        data.append(my_line)
    f1.close()

    f2 = open(query_path, 'r')
    query_lines = f2.readlines()
    query = []
    num_of_query = int(query_lines[1])
    for ii in range(2, len(query_lines)):
        cur_line = query_lines[ii]
        my_line = np.fromstring(cur_line, dtype=float, sep=' ')
        query.append(my_line)
    f2.close()

    all_index = []
    all_sims = []
    all_topk = []
    query = np.asarray(query)
    query = query.astype(np.float)

    for kk in range(len(query)):
        cur_query = query[kk]
        ground_truth = []
        for ii in range(size):
            x = data[ii].astype(np.float)
            # ground_truth = ground_truth + np.dot(cur_query, x).tolist()
            ground_truth.append(np.dot(cur_query, x))
        ground_truth = np.asarray(ground_truth)
        index = ground_truth.argsort()[::-1][:10]
        similarity = itemgetter(*index)(ground_truth)
        top_k_data = itemgetter(*index)(data)
        all_index.append(index)
        all_sims.append(similarity)
        all_topk.append(top_k_data)
    return all_topk, all_index, all_sims


# save struct to file
def persist_on_file(file_name, struct):
    myFile = open(file_name, 'w')
    for _list in struct:
        for _item in _list:
            myFile.write("%s" % str(_item))
        myFile.write("\n \n")
    myFile.close()


if __name__ == '__main__':
    layers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    # data_type = ['anti_correlated_']
    data_type = ['anti_correlated_', 'correlated_', 'random_']
    dimensions = [5]
    cardinality = [10000, 20000, 50000, 100000]
    topK = 10
    INPUT_DATA_FOLDER = '/Users/sicongliu/Desktop/StreamingTopK/H2_ALSH/raw_data/Synthetic/'
    QUERY_DATA_FOLDER = '/Users/sicongliu/Desktop/StreamingTopK/H2_ALSH/query/'
    OUTPUT_FOLDER = '/Users/sicongliu/Desktop/StreamingTopK/H2_ALSH/query/'
    LAYER_DATA_FOLDER = '/Users/sicongliu/Desktop/StreamingTopK/H2_ALSH/qhull_data/Synthetic/'
    # LAYER_DATA_FOLDER = '/Users/sliu104/Dropbox (ASU)/LSH_Synthetic/qhull_data/Synthetic/'
    for i in range(len(dimensions)):
        for j in range(len(cardinality)):
            for k in range(len(data_type)):
                data_file_name = INPUT_DATA_FOLDER + data_type[k] + str(dimensions[i]) + "_" + str(cardinality[j]) + \
                                 ".txt"
                query_file_name = QUERY_DATA_FOLDER + "query_" + str(dimensions[i]) + "D.txt"
                print("data name: " + data_file_name)
                print("query name: " + query_file_name)
                cur_data, cur_index, cur_similarity = computeTopK_All_Data(data_file_name, dimensions[i], cardinality[j], query_file_name)

                all_ground_truth = []

                # among layers search topk
                for ii in range(len(cur_similarity)):

                    return_struct = []
                    for m in range(len(layers)):

                        layer_file_path = LAYER_DATA_FOLDER + data_type[k] + str(dimensions[i]) + "_" + str(cardinality[j])\
                                        + "_qhull_layer_" + str(layers[m])
                        temp_result_struct = serachTopK(layer_file_path, cur_data[ii], cur_index[ii], cur_similarity[ii], layers[m])
                        if len(temp_result_struct) > 0:
                            return_struct = return_struct + temp_result_struct
                    # all_ground_truth.append(return_struct)
                    all_ground_truth = all_ground_truth + return_struct
                # save return_struct to file
                save_file_path = '/Users/sicongliu/Desktop/StreamingTopK/H2_ALSH/result/' + "grounTruth_Layer_Index_" + \
                                 data_type[k] + str(dimensions[i]) + "_" + str(cardinality[j])
                np.savetxt(save_file_path, all_ground_truth, fmt='%10.5f')
                # for ii in range(len(all_ground_truth)):
                    # np.savetxt(save_file_path, all_ground_truth[ii], fmt='%10.5f')
                    # temp = [0, 0, 0, 0, 0, 0]
                    # np.savetxt(save_file_path, temp, newline='\n')
                print("Done")