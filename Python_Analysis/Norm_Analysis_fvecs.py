import numpy as np


def fvecs_read(filename, c_contiguous=True):
    fv = np.fromfile(filename, dtype=np.float32)
    if fv.size == 0:
        return np.zeros((0, 0))
    dim = fv.view(np.int32)[0]
    assert dim > 0
    fv = fv.reshape(-1, 1 + dim)
    if not all(fv.view(np.int32)[:, 0] == dim):
        raise IOError("Non-uniform vector sizes in " + filename)
    fv = fv[:, 1:]
    if c_contiguous:
        fv = fv.copy()
    return fv


def save_file(input_file_name, save_file_folder):
    total_feature = fvecs_read(input_file_name)
    print(total_feature.__len__())
    print(total_feature.shape)
    total_count = total_feature.shape[0]
    num_of_dimension = total_feature.shape[1]

    save_file = save_file_folder + 'random_' + str(num_of_dimension) + '_' + str(total_count)
    total_feature = np.asarray(total_feature, dtype=np.float)
    total_feature = total_feature.transpose()

    total_data = []
    total_data.append(np.asarray(int(num_of_dimension)))
    total_data.append(np.asarray(int(total_count)))
    total_data = np.asarray(total_data)
    np.savetxt(save_file, total_data, delimiter=',', fmt='%i')

    total_feature = total_feature.transpose()
    f_handle = open(save_file, 'ab')
    # np.savetxt(f_handle, total_feature, fmt='%10.6f')
    np.savetxt(f_handle, total_feature)
    f_handle.close()
    return num_of_dimension, total_count


data_file = '/Users/sliu104/Downloads/netflix_base.fvecs'
query_file = '/Users/sliu104/Downloads/netflix_query.fvecs'

save_data_folder = "/Users/sliu104/Desktop/StreamingTopK/H2_ALSH/raw_data/Synthetic/"
save_query_folder = "/Users/sliu104/Desktop/StreamingTopK/H2_ALSH/query/"

data_dim, data_card = save_file(data_file, save_data_folder)
query_dim, query_card = save_file(query_file, save_query_folder)

print("merging features done")

chunks = 20
top_k = 25
query_num = query_card
data_folder = '/Users/sicongliu/Desktop/StreamingTopK/H2_ALSH/raw_data/Synthetic/'
query_folder = '/Users/sicongliu/Desktop/StreamingTopK/H2_ALSH/query/'
# data_type = ['anti_correlated_', 'correlated_', 'random_']
data_type = 'random_'
dimension = data_dim
cardinality = data_card

file_name = data_folder + data_type + str(dimension) + '_' + str(cardinality) + '.txt'
f = open(file_name, 'r')
lines = f.readlines()

cur_dim = int(lines[0])
cur_card = int(lines[1])
data_norm_list = []
data_list = []
for kk in range(cur_card):
    current_data_record = np.fromstring(lines[kk + 2], dtype=float, sep=' ')
    current_data_record = np.asarray(current_data_record)
    data_list.append(current_data_record)
    # temp_norm = float(format(np.linalg.norm(current_data_record), '.7f'))
    temp_norm = np.linalg.norm(current_data_record)
    data_norm_list.append(temp_norm)
f.close()
data_norm_list = np.asarray(data_norm_list)

query_file_name = query_folder + 'query_' + str(dimension) + 'D.txt'
f = open(query_file_name, 'r')
lines = f.readlines()
cur_dim = int(lines[0])
cur_card = int(lines[1])
query_list = []
for kk in range(cur_card):
    current_query_record = np.fromstring(lines[kk + 2], dtype=float, sep=' ')
    current_query_record = np.asarray(current_query_record)
    # temp_norm = np.linalg.norm(current_data_record)
    query_list.append(current_query_record)
f.close()
query_list = np.asarray(query_list)

# ==================== load data into bin ====================
min_norm = min(data_norm_list)
max_norm = max(data_norm_list)
norm_range = float(max_norm) - float(min_norm)
bin_size = norm_range / chunks

bin_array = []
cur_norm = float(min_norm)

while float(cur_norm) <= float(max_norm):
    bin_array.append(cur_norm)
    cur_norm = cur_norm + bin_size

# bin_array[0] = min(min_norm - 0.000001, bin_array[0] - 0.000001)
print(bin_array.__len__())
if bin_array.__len__()  == chunks and bin_array[bin_array.__len__() - 1] < max_norm:
    bin_array.append(bin_array[bin_array.__len__() - 1] + bin_size)
elif bin_array[bin_array.__len__() - 1] <= max_norm:
    bin_array[bin_array.__len__() - 1] = max(max_norm + 0.0000001, bin_array[bin_array.__len__() - 1] + 0.0000001)
# bin_array[bin_array.__len__() - 1] = max(max_norm + 0.0000001, bin_array[bin_array.__len__() - 1] + 0.0000001)

print(bin_array.__len__())
print(bin_array)

bins = np.array(bin_array)
# cur_bins = np.histogram(data_norm_list, bins)
# bins_count = cur_bins[0]
# bins_range = cur_bins[1]
# print(bins_count)
# plt.hist(norm_list, normed=True, bins=30)
# plt.ylabel('Probability')

# ==================== check top-25 how many elements in which bin ====================
total_counter = Counter()
for ii in range(query_num):
    print("Query index: " + str(ii))
    cur_query = query_list[ii]
    inner_prod_list = []
    # temp_data_norm_list = data_norm_list
    # temp_data_norm_list = np.asarray(temp_data_norm_list)
    for jj in range(cardinality):
        cur_data = data_list[jj]
        temp_dot_product = dot(cur_data, cur_query)
        inner_prod_list.append(temp_dot_product)
    inner_prod_list = np.asarray(inner_prod_list)
    reverse_sort_index = np.argsort((-inner_prod_list))
    top_k_index = reverse_sort_index[0: top_k]

    selected_norms = data_norm_list[list(top_k_index)]
    selected_inner_prod = inner_prod_list[list(top_k_index)]
    bin_count_array = np.digitize(selected_norms, bins)
    temp_counter = Counter(bin_count_array)
    total_counter = total_counter + temp_counter

plt.bar(total_counter.keys(), total_counter.values())

print('Done')
