import numpy as np
from operator import itemgetter


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
    print("search done")
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
    for ii in range(2, len(query_lines)):
        cur_line = query_lines[ii]
        my_line = np.fromstring(cur_line, dtype=float, sep=' ')
        query.append(my_line)
    f2.close()

    ground_truth = []
    query = np.asarray(query)
    query = query.astype(np.float)
    for ii in range(size):
        x = data[ii].astype(np.float)
        ground_truth = ground_truth + np.dot(query, x).tolist()
    ground_truth = np.asarray(ground_truth)
    index = ground_truth.argsort()[::-1][:10]
    similarity = itemgetter(*index)(ground_truth)
    top_k_data = itemgetter(*index)(data)
    return top_k_data, index, similarity


# save struct to file
def persist_on_file(file_name, struct):
    myFile = open(file_name, 'w')
    for _list in struct:
        for _item in _list:
            myFile.write("%s" % str(_item))
        myFile.write("\n \n")
    myFile.close()


if __name__ == '__main__':
    layers = [0, 1, 2, 3]
    data_type = ['anti_correlated_', 'correlated_', 'random_']
    dimensions = [5]
    cardinality = [1000, 2000, 4000, 8000]
    topK = 10
    INPUT_DATA_FOLDER = '/Users/sliu104/Desktop/StreamingTopK/H2_ALSH/raw_data/Synthetic/'
    QUERY_DATA_FOLDER = '/Users/sliu104/Desktop/StreamingTopK/H2_ALSH/query/'
    OUTPUT_FOLDER = '/Users/sliu104/Desktop/StreamingTopK/H2_ALSH/query/'
    LAYER_DATA_FOLDER = '/Users/sliu104/Desktop/StreamingTopK/H2_ALSH/qhull_data/Synthetic/'

    for i in range(len(dimensions)):
        for j in range(len(cardinality)):
            for k in range(len(data_type)):
                data_file_name = INPUT_DATA_FOLDER + data_type[k] + str(dimensions[i]) + "_" + str(cardinality[j]) + \
                                 ".txt"
                query_file_name = QUERY_DATA_FOLDER + "query_" + str(dimensions[i]) + "D.txt"
                print("data name: " + data_file_name)
                print("query name: " + query_file_name)
                cur_data, cur_index, cur_similarity = computeTopK_All_Data(data_file_name, dimensions[i], cardinality[j], query_file_name)

                # among layers search topk
                return_struct = []
                for m in range(len(layers)):
                    layer_file_path = LAYER_DATA_FOLDER + data_type[k] + str(dimensions[i]) + "_" + str(cardinality[j])\
                                      + "_qhull_layer_" + str(layers[m])
                    temp_result_struct = serachTopK(layer_file_path, cur_data, cur_index, cur_similarity, layers[m])
                    if len(temp_result_struct) > 0:
                        return_struct = return_struct + temp_result_struct
                # save return_struct to file
                save_file_path = '/Users/sliu104/Desktop/StreamingTopK/H2_ALSH/result/' + "grounTruth_Layer_Index_" + \
                                 data_type[k] + str(dimensions[i]) + "_" + str(cardinality[j])
                # persist_on_file(save_file_path, return_struct)
                np.savetxt(save_file_path, return_struct, fmt='%10.5f')
                print("Done")