import numpy as np


def read_raw_data(input_path):
    f = open(input_path, 'r')
    lines = f.readlines()
    first_line = lines[0]
    second_line = lines[1]

    cur_dimension = int(first_line.split('\n')[0])
    cur_cardinality = int(second_line.split('\n')[0])
    data = []
    for i in range(2, len(lines)):
        cur_line = lines[i]
        my_line = np.fromstring(cur_line, dtype=float, sep=' ')
        data.append(my_line)

    data = np.asarray(data)
    # print(type(data))
    f.close()
    return data


def read_temp_data(input_path):
    f = open(input_path, 'r')
    lines = f.readlines()
    data = []
    for i in range(len(lines)):
        cur_line = lines[i]
        my_line = np.fromstring(cur_line, dtype=float, sep=' ')
        data.append(my_line)

    data = np.asarray(data)
    # print(str(type(data)))
    f.close()
    return data


def search_index(sim_data, raw_data, sample_sim_value_file):
    my_index = []
    sampled_data_row = len(sim_data)
    sampled_data_column = len(sim_data[0])

    raw_data_row = len(raw_data)
    raw_data_column = len(raw_data[0])

    my_value = sim_data[:, len(sim_data[0]) - 1]
    sim_data = sim_data[:, 0: len(sim_data[0]) - 1]
    my_index = []

    cripped_index = []
    # for data in sim_data:
    for ii in range(len(sim_data)):
        my_row = np.where((raw_data == sim_data[ii]).all(axis=1))[0]
        if len(my_row) == 0:
            cripped_index.append(ii)
            continue
        my_index.append(my_row[0])
        # print(my_row[0])

    f = open(sample_sim_value_file, 'w')

    # flush zip pair to file
    my_value = np.delete(my_value, cripped_index, 0)
    print(len(my_index) == len(my_value))
    for idx, value in zip(my_index, my_value):
        # write this to file
        f.write(str(idx) + ' ' + str(value) + '\n')
    f.close()
    return 0


BASE_DIR = '/Users/sicongliu/Desktop/StreamingTopK/H2_ALSH/'
sample_space = 5
types = ['log', 'log_minus', 'log_plus', 'log_plus_plus', 'log_uni']
opt_types = ['opt', 'max', 'uni']
data_types = ['random']

dimensions = [4]
cardinalities = [1000000]
thresholds = ['without_threshold']
topks = [1, 2, 5, 10, 25]
max_topks = [25]

for data_type in data_types:
    for dimension in dimensions:
        for cardinality in cardinalities:
            for sample_index in range(sample_space):
                raw_data_file = BASE_DIR + 'raw_data/Synthetic/' + data_type + '_' + str(dimension) + '_' +\
                                str(cardinality) + '/' + data_type + '_' + str(dimension) + '_' + str(cardinality) + \
                                '_sample_' + str(sample_index) + '.txt'
                print('raw_data_file: ' + raw_data_file)
                # read raw data file
                raw_data = read_raw_data(raw_data_file)
                for type in types:
                    for opt_type in opt_types:
                        for max_topk in max_topks:
                            temp_result_dir = BASE_DIR + 'temp_result_' + str(dimension) + 'D_top' + str(max_topk) + \
                                              "_budget_10M_" + type + '_' + str(cardinality) + '_' + str(sample_index) + '/'
                            # print("temp_result_dir: " + temp_result_dir)
                            for topk in topks:
                                for threshold in thresholds:
                                    temp_result_file = temp_result_dir + 'run_test_' + data_type + '_' + str(dimension) \
                                                       + '_' + str(cardinality) + '_' + opt_type + '_' + str(sample_index) + \
                                                       '_top_' + str(topk) + '_' + threshold + '_' + str(sample_index) + '.txt'
                                    print(temp_result_file)
                                    # read temp file
                                    temp_data = read_temp_data(temp_result_file)
                                    # find index, persist on file
                                    sample_sim_value_file = temp_result_dir + data_type + '_' + str(dimension) \
                                                       + '_' + str(cardinality) + '_' + opt_type + '_' + str(sample_index) + \
                                                       '_top_' + str(topk) + '_' + threshold + '_' + str(sample_index) + '.txt'
                                    search_index(temp_data, raw_data, sample_sim_value_file)
print("All Done")


