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


file_name = '/Users/sliu104/Downloads/netflix_base.fvecs'
total_feature = fvecs_read(file_name)
print(total_feature.__len__())
print(total_feature.shape)
total_count = total_feature.shape[0]
num_of_dimension = total_feature.shape[1]

total_feature = np.asarray(total_feature, dtype=np.float)
total_feature = total_feature.transpose()

save_folder = "/Users/sliu104/Desktop/StreamingTopK/H2_ALSH/raw_data/Synthetic/"
save_file = save_folder + "random_300_" + str(total_count)

total_data = []
total_data.append(np.asarray(int(num_of_dimension)))
total_data.append(np.asarray(int(total_count)))
total_data = np.asarray(total_data)
np.savetxt(save_file, total_data, delimiter=',', fmt='%i')

f_handle = open(save_file, 'ab')
# np.savetxt(f_handle, total_feature, fmt='%10.6f')
np.savetxt(f_handle, total_feature)
f_handle.close()

print("merging features done")
