# data_type = ["anti_correlated", "correlated", "random"]
data_type = ["correlated"]
dimensions = [2, 5]
cardinality = [10000, 20000, 50000, 100000]
query_count = [20, 50]
topk = 10
hashTables = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
KList = [90, 80, 70, 60, 50, 40, 30, 20, 10, 10]

# count, hashTables KList
SCRIPT_OUTPUT_FILE = "../H2_ALSH/parameters/Mathematica_Parameters.txt"
DATA_FOLDER = "../H2_ALSH/qhull_data/Synthetic/"
f = open(SCRIPT_OUTPUT_FILE, 'w')

for i in range(len(data_type)):
    for j in range(len(dimensions)):
        for k in range(len(cardinality)):

            declare_string = data_type[i] + "_" + str(dimensions[j]) + "_" + str(cardinality[k])
            count = []
            f.write("# ------------------------------------------------------------------------------ \n")
            f.write("#     " + declare_string + " \n")
            f.write("# ------------------------------------------------------------------------------ \n")
            for m in range(topk):
                input_file = DATA_FOLDER + data_type[i] + "_" + str(dimensions[j]) + "_" + str(cardinality[k]) + \
                             "_qhull_layer_" + str(m)
                f1 = open(input_file, 'r')
                lines = f1.readlines()
                first_line = lines[0]
                second_line = lines[1]

                cur_dimension = int(first_line.split('\n')[0])
                cur_cardinality = int(second_line.split('\n')[0])
                assert cur_dimension == dimensions[j]

                count.append(float(cur_cardinality)/float(cardinality[k]))
                f1.close()
            f.write("count = List" + str(count) + "\n")
            f.write("hashTables = List[" + ','.join(hashTables) + "] \n")
            # f.write("hashTables = List" + str(hashTables) + "\n")
            f.write("KList = List" + str(KList) + "\n")
            f.write("\n \n \n")
f.close()





