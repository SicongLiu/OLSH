import numpy as np


# load data
def load_sample(input_path, output_dir, total_dim, sample_dim, reps):
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
        dim_index = np.random.choice(total_dim, sample_dim, replace=False)
        print("dim_index: ", dim_index)

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
    dimension = 5
    cardinality = 1000
    data_type = 'random_'
    MAX_LAYERS = 10

    input_path = "/Users/sicongliu/Desktop/StreamingTopK/Python_Analysis/random_" + str(dimension) + "_1000.txt"
    output_dir = "/Users/sicongliu/Desktop/StreamingTopK/Python_Analysis/"

    reps = 3
    sample_dim = 3

    # sample data
    assert(sample_dim <= dimension)
    load_sample(input_path, output_dir, dimension, sample_dim, reps)

    # sample query
    input_path = "/Users/sicongliu/Desktop/StreamingTopK/Python_Analysis/random_" + str(dimension) + "_1000.txt"
    output_dir = "/Users/sicongliu/Desktop/StreamingTopK/Python_Analysis/"

    load_sample(input_path, output_dir, dimension, sample_dim, reps)
    print("input_path: ", input_path)
    print("Done.")



