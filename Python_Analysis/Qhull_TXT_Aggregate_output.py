# output qhull aggregation information, for loading into excel purpose


def read_card(file_name_):
    f = open(file_name_, 'r')
    lines = f.readlines()
    first_line = lines[0]
    second_line = lines[1]
    f.close()
    return second_line


def print_list(list_):
    for ii in list_:
        print(ii)


top_k = 25

dims = [2, 3, 5, 6, 7]
data_folder = "/home/cc/Chameleon/StreamingTopK/H2_ALSH/qhull_data/Synthetic/"
for i in dims:
    anti_list = []
    cor_list = []
    random_list = []
    for j in range(top_k):
        # anti_correlated_7_500000_qhull_layer_4
        anti_cor = data_folder + "anti_correlated_" + str(i) + '_500000_qhull_layer_' + str(j)
        anti_list.append(read_card(anti_cor))

        cor = data_folder + "correlated_" + str(i) + '_500000_qhull_layer_' + str(j)
        cor_list.append(read_card(cor))

        random = data_folder + "random_" + str(i) + '_500000_qhull_layer_' + str(j)
        random_list.append(read_card(random))

    print("dim: ", i)
    print("========= anti_correlated =======")
    print_list(anti_list)

    print("========= correlated =======")
    print_list(cor_list)

    print("========= random =======")
    print_list(random_list)

print("all done")







