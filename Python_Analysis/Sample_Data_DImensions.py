import numpy as np


# load data
def load_sample_data(input_path, output_dir, total_dim, sample_dim, reps):
    f = open(input_path, 'r')
    lines = f.readlines()
    first_line = lines[0]
    second_line = lines[1]

    cur_dimension = int(first_line.split('\n')[0])

    assert(cur_dimension == total_dim)
    cur_cardinality = int(second_line.split('\n')[0])
    data = []
    for i in range(2, len(lines)):
        cur_line = lines[i]
        my_line = np.fromstring(cur_line, dtype=float, sep=' ')
        data.append(my_line)

    data = np.asarray(data)
    print(type(data))

    sample_index_list = list()
    for i in range(reps):
        dim_index = np.random.choice(total_dim, sample_dim, replace=False)
        print("Current data reps: ", i, " dim_index: ", dim_index)

        sample_index_list.append(dim_index)

        output_path = output_dir + str(i) + ".txt"
        # extra dim_index and output data

        temp_data = []
        for dim_of_interest in dim_index:
            if np.shape(temp_data)[0] == 0:
                temp_data = data[:, [dim_of_interest]]
            else:
                temp_data = np.hstack((temp_data, data[:, [dim_of_interest]]))

        data_header = []
        data_header.append(np.asarray(int(sample_dim)))
        data_header.append(np.asarray(int(cur_cardinality)))
        data_header = np.asarray(data_header)
        np.savetxt(output_path, data_header, delimiter=',', fmt='%i')

        f_handle = open(output_path, 'ab')
        np.savetxt(f_handle, temp_data, fmt='%10.6f')
        f_handle.close()
    return sample_index_list


# use the same sampled dimensions from down sampling data
def load_sample_query(input_path, output_dir, total_dim, sample_dim, reps, sample_index_list):
    f = open(input_path, 'r')
    lines = f.readlines()
    first_line = lines[0]
    second_line = lines[1]

    cur_dimension = int(first_line.split('\n')[0])

    assert(cur_dimension == total_dim)
    cur_cardinality = int(second_line.split('\n')[0])
    data = []
    for i in range(2, len(lines)):
        cur_line = lines[i]
        my_line = np.fromstring(cur_line, dtype=float, sep=' ')
        data.append(my_line)

    data = np.asarray(data)
    print(type(data))

    for i in range(reps):
        # dim_index = np.random.choice(total_dim, sample_dim, replace=False)
        dim_index = sample_index_list[i]
        print("Current query reps: ", i, " dim_index: ", dim_index)

        output_path = output_dir + str(i) + ".txt"
        # extra dim_index and output data

        temp_data = []
        for dim_of_interest in dim_index:
            if np.shape(temp_data)[0] == 0:
                temp_data = data[:, [dim_of_interest]]
            else:
                temp_data = np.hstack((temp_data, data[:, [dim_of_interest]]))

        data_header = []
        data_header.append(np.asarray(int(sample_dim)))
        data_header.append(np.asarray(int(cur_cardinality)))
        data_header = np.asarray(data_header)
        np.savetxt(output_path, data_header, delimiter=',', fmt='%i')

        f_handle = open(output_path, 'ab')
        np.savetxt(f_handle, temp_data, fmt='%10.6f')
        f_handle.close()


if __name__ == '__main__':
    dimension = 7
    cardinality = 1000000
    data_type = 'random_'

    # MAX_LAYERS = 50
    reps = 10
    sample_dim = 4

    # sample data
    # input_path = "/Users/sicongliu/Desktop/StreamingTopK/Python_Analysis/random_" + str(dimension) + "_" + str(cardinality) + ".txt"
    input_path = "/Users/sicongliu/Desktop/StreamingTopK/H2_ALSH/raw_data/Synthetic/random_" + str(dimension) + "_" + str(
        cardinality) + ".txt"
    output_dir = "/Users/sicongliu/Desktop/StreamingTopK/H2_ALSH/raw_data/Synthetic/random_" + str(sample_dim) + "_" + str(cardinality) + '/'

    assert(sample_dim <= dimension)
    print("input_path: ", input_path)
    sample_index_list = load_sample_data(input_path, output_dir, dimension, sample_dim, reps)

    # sample query
    query_path = "/Users/sicongliu/Desktop/StreamingTopK/H2_ALSH/query/query_" + str(dimension) + "D.txt"
    output_query_dir = "/Users/sicongliu/Desktop/StreamingTopK/H2_ALSH/query/"

    print("query_path: ", query_path)
    load_sample_query(query_path, output_query_dir, dimension, sample_dim, reps, sample_index_list)

    print("Done.")



